from django.utils.functional import LazyObject

__version__ = '1.1.1'

default_app_config = 'constance.apps.ConstanceConfig'


class LazyConfig(LazyObject):
    def _setup(self):
        from .base import Config
        self._wrapped = Config()

config = LazyConfig()
