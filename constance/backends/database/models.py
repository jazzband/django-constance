from django.db import models
from django.core.exceptions import ImproperlyConfigured

from django.utils.translation import gettext_lazy as _

try:
    from picklefield import PickledObjectField
except ImportError:
    raise ImproperlyConfigured("Couldn't find the the 3rd party app "
                               "django-picklefield which is required for "
                               "the constance database backend.")


class Constance(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = PickledObjectField(null=True, blank=True)

    class Meta:
        verbose_name = _('constance')
        verbose_name_plural = _('constances')
        db_table = 'constance_config'

    def __str__(self):
        return self.key
