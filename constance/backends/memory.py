from threading import Lock

from constance import config
from constance import signals

from . import Backend


class MemoryBackend(Backend):
    """Simple in-memory backend that should be mostly used for testing purposes."""

    _storage = {}
    _lock = Lock()

    def __init__(self):
        super().__init__()

    def get(self, key):
        with self._lock:
            return self._storage.get(key)

    async def aget(self, key):
        # Memory operations are fast enough that we don't need true async here
        return self.get(key)

    def mget(self, keys):
        if not keys:
            return None
        result = []
        with self._lock:
            for key in keys:
                value = self._storage.get(key)
                if value is not None:
                    result.append((key, value))
        return result

    async def amget(self, keys):
        if not keys:
            return {}
        with self._lock:
            return {key: self._storage[key] for key in keys if key in self._storage}

    def set(self, key, value):
        with self._lock:
            old_value = self._storage.get(key)
            self._storage[key] = value
            signals.config_updated.send(sender=config, key=key, old_value=old_value, new_value=value)

    async def aset(self, key, value):
        # Memory operations are fast enough that we don't need true async here
        self.set(key, value)
