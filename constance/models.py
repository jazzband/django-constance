from django.db import models
from django.utils.translation import gettext_lazy as _


class Constance(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField(null=True, blank=True, editable=False)

    class Meta:
        verbose_name = _('constance')
        verbose_name_plural = _('constances')
        permissions = [
            ('change_config', 'Can change config'),
            ('view_config', 'Can view config'),
        ]

    def __str__(self):
        return self.key
