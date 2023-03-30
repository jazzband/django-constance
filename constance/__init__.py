from django.utils.functional import LazyObject

__version__ = '2.9.1'


class LazyConfig(LazyObject):
    def _setup(self):
        from .base import Config
        self._wrapped = Config()


config = LazyConfig()
