from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save
from django.utils.functional import memoize

from constance.backends import Backend

db_cache = {}

class DatabaseBackend(Backend):

    def __init__(self):
        from constance.backends.database.models import Constance
        if not Constance._meta.installed:
            raise ImproperlyConfigured(
                "The constance.contrib.database app isn't installed correctly. "
                "Make sure it's listed in the INSTALLED_APPS setting.")
        self._model = Constance
        # Clear simple cache.
        post_save.connect(self.clear, sender=self._model)

    def _get(self, key):
        try:
            value = self._model._default_manager.get(key=key).value
        except self._model.DoesNotExist:
            return None
        return value
    get = memoize(_get, db_cache, 2)

    def set(self, key, value):
        constance, created = self._model._default_manager.get_or_create(key=key, defaults={'value': value})
        if not created:
            constance.value = value
            constance.save()

    def clear(self, sender, instance, created, **kwargs):
        if not created:
            db_cache.clear()
