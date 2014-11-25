from .base import Config

__version__ = '1.0a1'

try:
    from django.apps import AppConfig  # noqa
except ImportError:
    config = Config()
else:
    default_app_config = 'constance.apps.ConstanceConfig'
