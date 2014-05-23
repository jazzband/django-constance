from django.apps import AppConfig
from constance.config import Config


class ConstanceConfig(AppConfig):
    name = 'constance'
    verbose_name = 'Constance'

    def ready(self):
        self.module.config = Config()
