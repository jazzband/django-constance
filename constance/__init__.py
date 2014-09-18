import django

major_version = django.VERSION[0]
minor_version = django.VERSION[1]

if major_version >= 1 and minor_version >= 7:
    from django.apps import AppConfig
    default_app_config = 'constance.apps.ConstanceConfig'
else:
    from constance.config import Config
    config = Config()