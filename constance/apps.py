from django.apps import AppConfig
from django.core import checks
from django.utils.translation import gettext_lazy as _

from constance.checks import check_fieldsets


class ConstanceConfig(AppConfig):
    name = 'constance'
    verbose_name = _('Constance')
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        checks.register(check_fieldsets, 'constance')
