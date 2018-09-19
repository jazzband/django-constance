from django.conf import settings

from . import Backend


class DummyBackend(Backend):

    def mget(self, keys):
        return {key: self.get(key) for key in keys}

    def get(self, key):
        return settings.CONSTANCE_CONFIG.get(key, (None,))[0]

    def set(self, key, value):
        """Don't do that!"""
        raise NotImplementedError
