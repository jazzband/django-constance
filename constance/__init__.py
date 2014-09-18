import django

if django.VERSION >= (1,7):
    from django.apps import AppConfig
    default_app_config = 'constance.apps.ConstanceConfig'
else:
    from constance.config import Config
    config = Config()