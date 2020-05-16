from threading import Lock

from . import Backend
from .. import signals, config


class MemoryBackend(Backend):
    """
    Simple in-memory backend that should be mostly used for testing purposes
    """
    def __init__(self):
        super().__init__()
        self._storage = {}
        self._lock = Lock()

    def get(self, key):
        return self._storage.get(key)

    def mget(self, keys):
        if not keys:
            return
        result = []
        with self._lock:
            for key in keys:
                value = self._storage.get(key)
                if value is not None:
                    result.append((key, value))
        return result

    def set(self, key, value):
        old_value = self.get(key)
        self._storage[key] = value
        signals.config_updated.send(
            sender=config, key=key, old_value=old_value, new_value=value
        )
