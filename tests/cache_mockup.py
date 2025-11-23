from typing import Any

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
