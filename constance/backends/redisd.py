import asyncio
from threading import RLock
from time import monotonic

from django.core.exceptions import ImproperlyConfigured

from constance import config
from constance import settings
from constance import signals
from constance import utils
from constance.backends import Backend
from constance.codecs import dumps
from constance.codecs import loads


class RedisBackend(Backend):
    def __init__(self):
        super().__init__()
        self._prefix = settings.REDIS_PREFIX
        connection_cls = settings.REDIS_CONNECTION_CLASS
        async_connection_cls = settings.REDIS_ASYNC_CONNECTION_CLASS

        if connection_cls:
            self._rd = utils.import_module_attr(connection_cls)()
        else:
            try:
                import redis
            except ImportError:
                raise ImproperlyConfigured("The Redis backend requires redis-py to be installed.") from None
            else:
                if isinstance(settings.REDIS_CONNECTION, str):
                    self._rd = redis.from_url(settings.REDIS_CONNECTION)
                else:
                    self._rd = redis.Redis(**settings.REDIS_CONNECTION)

        if async_connection_cls:
            self._ard = utils.import_module_attr(async_connection_cls)()
        else:
            try:
                import redis.asyncio as aredis
            except ImportError:
                # We set this to none instead of raising an error to indicate that async support is not available
                # without breaking existing sync usage.
                self._ard = None
            else:
                if isinstance(settings.REDIS_CONNECTION, str):
                    self._ard = aredis.from_url(settings.REDIS_CONNECTION)
                else:
                    self._ard = aredis.Redis(**settings.REDIS_CONNECTION)

    def add_prefix(self, key):
        return f"{self._prefix}{key}"

    def _check_async_support(self):
        if self._ard is None:
            raise ImproperlyConfigured(
                "Async support for the Redis backend requires redis>=4.2.0 "
                "or a custom CONSTANCE_REDIS_ASYNC_CONNECTION_CLASS to be configured."
            )

    def get(self, key):
        value = self._rd.get(self.add_prefix(key))
        if value:
            return loads(value)
        return None

    async def aget(self, key):
        self._check_async_support()
        value = await self._ard.get(self.add_prefix(key))
        if value:
            return loads(value)
        return None

    def mget(self, keys):
        if not keys:
            return
        prefixed_keys = [self.add_prefix(key) for key in keys]
        for key, value in zip(keys, self._rd.mget(prefixed_keys)):
            if value:
                yield key, loads(value)

    async def amget(self, keys):
        if not keys:
            return {}
        self._check_async_support()
        prefixed_keys = [self.add_prefix(key) for key in keys]
        values = await self._ard.mget(prefixed_keys)
        return {key: loads(value) for key, value in zip(keys, values) if value}

    def set(self, key, value):
        old_value = self.get(key)
        self._rd.set(self.add_prefix(key), dumps(value))
        signals.config_updated.send(sender=config, key=key, old_value=old_value, new_value=value)

    async def _aset_internal(self, key, value, old_value):
        """
        Internal set operation. Separated to allow subclasses to provide old_value
        without going through self.aget() which may have locking behavior.
        """
        self._check_async_support()
        await self._ard.set(self.add_prefix(key), dumps(value))
        signals.config_updated.send(sender=config, key=key, old_value=old_value, new_value=value)

    async def aset(self, key, value):
        old_value = await self.aget(key)
        await self._aset_internal(key, value, old_value)


class CachingRedisBackend(RedisBackend):
    _sentinel = object()
    _lock = RLock()
    _async_lock = None  # Lazy-initialized asyncio.Lock

    def __init__(self):
        super().__init__()
        self._timeout = settings.REDIS_CACHE_TIMEOUT
        self._cache = {}
        self._sentinel = object()

    def _get_async_lock(self):
        # Lazily create the asyncio lock to avoid issues with event loops
        if self._async_lock is None:
            self._async_lock = asyncio.Lock()
        return self._async_lock

    def _has_expired(self, value):
        return value[0] <= monotonic()

    def _cache_value(self, key, new_value):
        self._cache[key] = (monotonic() + self._timeout, new_value)

    def get(self, key):
        value = self._cache.get(key, self._sentinel)

        if value is self._sentinel or self._has_expired(value):
            with self._lock:
                new_value = super().get(key)
                self._cache_value(key, new_value)
                return new_value

        return value[1]

    async def _aget_unlocked(self, key):
        """
        Get value with cache support but without acquiring lock.
        Caller must already hold the lock.
        """
        value = self._cache.get(key, self._sentinel)
        if value is self._sentinel or self._has_expired(value):
            new_value = await super().aget(key)
            self._cache_value(key, new_value)
            return new_value
        return value[1]

    async def aget(self, key):
        value = self._cache.get(key, self._sentinel)

        if value is self._sentinel or self._has_expired(value):
            async with self._get_async_lock():
                # Double-check after acquiring lock, then delegate to unlocked version
                return await self._aget_unlocked(key)

        return value[1]

    def set(self, key, value):
        with self._lock:
            super().set(key, value)
            self._cache_value(key, value)

    async def aset(self, key, value):
        async with self._get_async_lock():
            # Use unlocked version since we already hold the lock
            old_value = await self._aget_unlocked(key)
            # Use internal method to avoid lock recursion (super().aset calls self.aget)
            await self._aset_internal(key, value, old_value)
            self._cache_value(key, value)

    def mget(self, keys):
        if not keys:
            return
        for key in keys:
            value = self.get(key)
            if value is not None:
                yield key, value

    async def amget(self, keys):
        if not keys:
            return {}

        results = {}
        missing_keys = []

        # First, check the local cache for all keys
        for key in keys:
            value = self._cache.get(key, self._sentinel)
            if value is not self._sentinel and not self._has_expired(value):
                results[key] = value[1]
            else:
                missing_keys.append(key)

        # Fetch missing keys from Redis
        if missing_keys:
            async with self._get_async_lock():
                # Re-check cache for keys that might have been fetched while waiting for lock
                still_missing = []
                for key in missing_keys:
                    value = self._cache.get(key, self._sentinel)
                    if value is not self._sentinel and not self._has_expired(value):
                        results[key] = value[1]
                    else:
                        still_missing.append(key)

                if still_missing:
                    fetched = await super().amget(still_missing)
                    for key, value in fetched.items():
                        self._cache_value(key, value)
                        results[key] = value

        return results
