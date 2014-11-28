from django.apps import AppConfig
from django.db import OperationalError
from django.utils.translation import ugettext_lazy as _

from .base import Config


class ConstanceConfig(AppConfig):
    name = 'constance'
    verbose_name = _('Constance')

    def ready(self):
        super(ConstanceConfig, self).ready()
        try:
            self.module.config = Config()
        except OperationalError:
            pass
