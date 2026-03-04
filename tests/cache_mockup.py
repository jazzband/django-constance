from django.core.cache.backends.base import BaseCache
from django.core.cache.backends.locmem import LocMemCache


class Cache(BaseCache):
    def __init__(self, name, params):
        self._cache = LocMemCache(name, params)
        self.add = self._cache.add
        self.delete = self._cache.delete
        self.set = self._cache.set
        self.get = self._cache.get
        self.clear = self._cache.clear
        self.set_many = self._cache.set_many
        self.get_many = self._cache.get_many
        self.delete_many = self._cache.delete_many

    # Async methods for DatabaseBackend.aget() support
    async def aget(self, key, default=None, version=None):
        return self.get(key, default, version)

    async def aget_many(self, keys, version=None):
        return self.get_many(keys, version)

    async def aadd(self, key, value, timeout=None, version=None):
        return self.add(key, value, timeout, version)
