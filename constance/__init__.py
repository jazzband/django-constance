from django.utils.functional import LazyObject


class LazyConfig(LazyObject):
    def _setup(self):
        from .base import Config

        self._wrapped = Config()


config = LazyConfig()
