from .base import Config
from django.utils.functional import SimpleLazyObject

__version__ = '1.0a1'


try:
    from django.apps import AppConfig  # noqa
except ImportError:
    config = SimpleLazyObject(Config)
else:
    default_app_config = 'constance.apps.ConstanceConfig'
