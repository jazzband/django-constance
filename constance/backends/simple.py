from . import Backend
from .. import signals, config


class SimpleBackend(Backend):

    def __init__(self):
        super().__init__()
        self._storage = {}

    def get(self, key):
        return self._storage.get(key)

    def mget(self, keys):
        if not keys:
            return
        for key in keys:
            value = self._storage.get(key)
            if value is not None:
                yield key, value

    def set(self, key, value):
        old_value = self.get(key)
        self._storage[key] = value
        signals.config_updated.send(
            sender=config, key=key, old_value=old_value, new_value=value
        )
