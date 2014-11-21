from django.apps import AppConfig
from constance.config import Config
from django.utils.translation import ugettext_lazy as _

class ConstanceConfig(AppConfig):
    name = 'constance'
    verbose_name = _('Constance')

    def ready(self):
        self.module.config = Config()
