from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConstanceConfig(AppConfig):
    name = 'constance.backends.database'
    label = 'constance_db'
    verbose_name = _('Constance Database Backend')
