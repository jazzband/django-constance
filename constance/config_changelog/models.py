from django.db import models
from picklefield import PickledObjectField

from constance.signals import config_updated


class ConfigLogEntry(models.Model):
    key = models.CharField(max_length=255)
    old_value = PickledObjectField()
    new_value = PickledObjectField()
    changed_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{0}: {1}->{2}'.format(self.key, self.old_value, self.new_value)


def log_config_change(sender, key, old_value, new_value, **kwargs):
    ConfigLogEntry.objects.create(
        key=key,
        old_value=old_value,
        new_value=new_value
    )


config_updated.connect(log_config_change, dispatch_uid='constance.log_config_change')
