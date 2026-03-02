from unittest import mock

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test import TransactionTestCase

from constance import settings
from constance.base import Config
from constance.backends.redisd import RedisBackend
from tests.storage import StorageTestsMixin


class TestRedis(StorageTestsMixin, TestCase):
    _BACKEND = "constance.backends.redisd.RedisBackend"

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = self._BACKEND
        super().setUp()
        self.config._backend._rd.clear()

    def tearDown(self):
        self.config._backend._rd.clear()
        settings.BACKEND = self.old_backend

    def test_mget_empty_keys(self):
        # Test that mget returns None for empty keys
        result = list(self.config._backend.mget([]) or [])
        self.assertEqual(result, [])


class TestCachingRedis(TestRedis):
    _BACKEND = "constance.backends.redisd.CachingRedisBackend"

    def test_mget_empty_keys(self):
        # Test that mget returns None for empty keys
        result = list(self.config._backend.mget([]) or [])
        self.assertEqual(result, [])


class TestRedisAsync(TransactionTestCase):
    _BACKEND = "constance.backends.redisd.RedisBackend"

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = self._BACKEND
        self.config = Config()
        self.config._backend._rd.clear()

    def tearDown(self):
        self.config._backend._rd.clear()
        settings.BACKEND = self.old_backend

    async def test_aget_returns_none_for_missing_key(self):
        result = await self.config._backend.aget("INT_VALUE")
        self.assertIsNone(result)

    async def test_aget_returns_value(self):
        self.config._backend.set("INT_VALUE", 42)
        result = await self.config._backend.aget("INT_VALUE")
        self.assertEqual(result, 42)

    async def test_aset_stores_value(self):
        await self.config._backend.aset("INT_VALUE", 99)
        result = self.config._backend.get("INT_VALUE")
        self.assertEqual(result, 99)

    async def test_amget_returns_empty_for_no_keys(self):
        result = await self.config._backend.amget([])
        self.assertEqual(result, {})

    async def test_amget_returns_values(self):
        self.config._backend.set("INT_VALUE", 10)
        self.config._backend.set("BOOL_VALUE", True)
        result = await self.config._backend.amget(["INT_VALUE", "BOOL_VALUE"])
        self.assertEqual(result, {"INT_VALUE": 10, "BOOL_VALUE": True})

    async def test_amget_skips_missing_keys(self):
        self.config._backend.set("INT_VALUE", 10)
        result = await self.config._backend.amget(["INT_VALUE", "MISSING_KEY"])
        self.assertEqual(result, {"INT_VALUE": 10})


class TestCachingRedisAsync(TransactionTestCase):
    _BACKEND = "constance.backends.redisd.CachingRedisBackend"

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = self._BACKEND
        self.config = Config()
        self.config._backend._rd.clear()
        self.config._backend._cache.clear()

    def tearDown(self):
        self.config._backend._rd.clear()
        self.config._backend._cache.clear()
        settings.BACKEND = self.old_backend

    async def test_aget_caches_value(self):
        # First set a value via sync
        self.config._backend.set("INT_VALUE", 42)
        # Clear the in-memory cache
        self.config._backend._cache.clear()

        # Async get should fetch and cache
        result = await self.config._backend.aget("INT_VALUE")
        self.assertEqual(result, 42)

        # Verify it's cached
        self.assertIn("INT_VALUE", self.config._backend._cache)

    async def test_aget_returns_cached_value(self):
        # Manually set cache
        from time import monotonic

        timeout = self.config._backend._timeout
        self.config._backend._cache["INT_VALUE"] = (monotonic() + timeout, 100)

        result = await self.config._backend.aget("INT_VALUE")
        self.assertEqual(result, 100)

    async def test_aget_refreshes_expired_cache(self):
        from time import monotonic

        # Set expired cache
        self.config._backend._cache["INT_VALUE"] = (monotonic() - 10, 100)
        # Set different value in redis using proper codec format
        self.config._backend._rd.set(
            self.config._backend.add_prefix("INT_VALUE"),
            b'{"__type__": "default", "__value__": 200}',
        )

        result = await self.config._backend.aget("INT_VALUE")
        self.assertEqual(result, 200)

    async def test_aset_updates_cache(self):
        await self.config._backend.aset("INT_VALUE", 55)

        # Verify cache is updated
        self.assertIn("INT_VALUE", self.config._backend._cache)
        self.assertEqual(self.config._backend._cache["INT_VALUE"][1], 55)

    async def test_amget_returns_empty_for_no_keys(self):
        result = await self.config._backend.amget([])
        self.assertEqual(result, {})

    async def test_amget_returns_cached_values(self):
        from time import monotonic

        timeout = self.config._backend._timeout
        self.config._backend._cache["INT_VALUE"] = (monotonic() + timeout, 10)
        self.config._backend._cache["BOOL_VALUE"] = (monotonic() + timeout, True)

        result = await self.config._backend.amget(["INT_VALUE", "BOOL_VALUE"])
        self.assertEqual(result, {"INT_VALUE": 10, "BOOL_VALUE": True})

    async def test_amget_fetches_missing_keys(self):
        from time import monotonic

        timeout = self.config._backend._timeout
        # One key cached, one in Redis only
        self.config._backend._cache["INT_VALUE"] = (monotonic() + timeout, 10)
        self.config._backend._rd.set(
            self.config._backend.add_prefix("BOOL_VALUE"),
            b'{"__type__": "default", "__value__": true}',
        )

        result = await self.config._backend.amget(["INT_VALUE", "BOOL_VALUE"])
        self.assertEqual(result["INT_VALUE"], 10)
        self.assertEqual(result["BOOL_VALUE"], True)

    async def test_amget_refreshes_expired_keys(self):
        from time import monotonic

        # Set expired cache
        self.config._backend._cache["INT_VALUE"] = (monotonic() - 10, 100)
        # Set different value in redis using proper codec format
        self.config._backend._rd.set(
            self.config._backend.add_prefix("INT_VALUE"),
            b'{"__type__": "default", "__value__": 200}',
        )

        result = await self.config._backend.amget(["INT_VALUE"])
        self.assertEqual(result["INT_VALUE"], 200)


class TestRedisBackendInit(TestCase):
    """Tests for RedisBackend.__init__ client initialization paths."""

    def setUp(self):
        self.old_conn_cls = settings.REDIS_CONNECTION_CLASS
        self.old_async_conn_cls = settings.REDIS_ASYNC_CONNECTION_CLASS
        self.old_conn = settings.REDIS_CONNECTION

    def tearDown(self):
        settings.REDIS_CONNECTION_CLASS = self.old_conn_cls
        settings.REDIS_ASYNC_CONNECTION_CLASS = self.old_async_conn_cls
        settings.REDIS_CONNECTION = self.old_conn

    def test_no_redis_package_raises_improperly_configured(self):
        settings.REDIS_CONNECTION_CLASS = None
        settings.REDIS_ASYNC_CONNECTION_CLASS = "tests.redis_mockup.AsyncConnection"
        with mock.patch.dict("sys.modules", {"redis": None}):
            with self.assertRaises(ImproperlyConfigured):
                RedisBackend()

    def test_sync_redis_from_url_with_string_connection(self):
        settings.REDIS_CONNECTION_CLASS = None
        settings.REDIS_ASYNC_CONNECTION_CLASS = "tests.redis_mockup.AsyncConnection"
        settings.REDIS_CONNECTION = "redis://localhost:6379/0"
        mock_redis = mock.MagicMock()
        with mock.patch.dict("sys.modules", {"redis": mock_redis, "redis.asyncio": mock_redis.asyncio}):
            backend = RedisBackend()
        mock_redis.from_url.assert_called_once_with("redis://localhost:6379/0")
        self.assertEqual(backend._rd, mock_redis.from_url.return_value)

    def test_sync_redis_with_dict_connection(self):
        settings.REDIS_CONNECTION_CLASS = None
        settings.REDIS_ASYNC_CONNECTION_CLASS = "tests.redis_mockup.AsyncConnection"
        settings.REDIS_CONNECTION = {"host": "localhost", "port": 6379}
        mock_redis = mock.MagicMock()
        with mock.patch.dict("sys.modules", {"redis": mock_redis, "redis.asyncio": mock_redis.asyncio}):
            backend = RedisBackend()
        mock_redis.Redis.assert_called_once_with(host="localhost", port=6379)
        self.assertEqual(backend._rd, mock_redis.Redis.return_value)

    def test_async_redis_not_available_sets_ard_none(self):
        settings.REDIS_CONNECTION_CLASS = "tests.redis_mockup.Connection"
        settings.REDIS_ASYNC_CONNECTION_CLASS = None
        mock_redis = mock.MagicMock()
        # Simulate redis.asyncio not being available
        with mock.patch.dict("sys.modules", {"redis": mock_redis, "redis.asyncio": None}):
            backend = RedisBackend()
        self.assertIsNone(backend._ard)

    def test_async_redis_from_url_with_string_connection(self):
        settings.REDIS_CONNECTION_CLASS = "tests.redis_mockup.Connection"
        settings.REDIS_ASYNC_CONNECTION_CLASS = None
        settings.REDIS_CONNECTION = "redis://localhost:6379/0"
        mock_aredis = mock.MagicMock()
        mock_redis = mock.MagicMock()
        mock_redis.asyncio = mock_aredis
        with mock.patch.dict("sys.modules", {"redis": mock_redis, "redis.asyncio": mock_aredis}):
            backend = RedisBackend()
        mock_aredis.from_url.assert_called_once_with("redis://localhost:6379/0")
        self.assertEqual(backend._ard, mock_aredis.from_url.return_value)

    def test_async_redis_with_dict_connection(self):
        settings.REDIS_CONNECTION_CLASS = "tests.redis_mockup.Connection"
        settings.REDIS_ASYNC_CONNECTION_CLASS = None
        settings.REDIS_CONNECTION = {"host": "localhost", "port": 6379}
        mock_aredis = mock.MagicMock()
        mock_redis = mock.MagicMock()
        mock_redis.asyncio = mock_aredis
        with mock.patch.dict("sys.modules", {"redis": mock_redis, "redis.asyncio": mock_aredis}):
            backend = RedisBackend()
        mock_aredis.Redis.assert_called_once_with(host="localhost", port=6379)
        self.assertEqual(backend._ard, mock_aredis.Redis.return_value)

    def test_check_async_support_raises_when_ard_is_none(self):
        backend = RedisBackend()
        backend._ard = None
        with self.assertRaises(ImproperlyConfigured):
            backend._check_async_support()
