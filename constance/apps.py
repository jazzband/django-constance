from django.apps import AppConfig
from constance.config import Config
from django.utils.translation import ugettext as _

class ConstanceConfig(AppConfig):
    name = 'constance'
    verbose_name = _('Constance')

    def ready(self):
        self.module.config = Config()
