import django
from django.utils.functional import LazyObject
from . import checks

__version__ = '2.9.1'

if django.VERSION < (3, 2):  # pragma: no cover
    default_app_config = 'constance.apps.ConstanceConfig'


class LazyConfig(LazyObject):
    def _setup(self):
        from .base import Config
        self._wrapped = Config()


config = LazyConfig()
