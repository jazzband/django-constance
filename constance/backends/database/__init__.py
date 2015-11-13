from django.core.cache import caches
from django.core.cache.backends.locmem import LocMemCache
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save

from .. import Backend
from ... import settings


class DatabaseBackend(Backend):
    def __init__(self):
        from .models import Constance
        self._model = Constance
        self._prefix = settings.DATABASE_PREFIX
        self._autofill_timeout = settings.DATABASE_CACHE_AUTOFILL_TIMEOUT
        self._autofill_cachekey = 'autofilled'

        if not self._model._meta.installed:
            raise ImproperlyConfigured(
                "The constance.backends.database app isn't installed "
                "correctly. Make sure it's in your INSTALLED_APPS setting.")

        if settings.DATABASE_CACHE_BACKEND:
            self._cache = caches[settings.DATABASE_CACHE_BACKEND]
            if isinstance(self._cache, LocMemCache):
                raise ImproperlyConfigured(
                    "The CONSTANCE_DATABASE_CACHE_BACKEND setting refers to a "
                    "subclass of Django's local-memory backend (%r). Please set "
                    "it to a backend that supports cross-process caching."
                    % settings.DATABASE_CACHE_BACKEND)
        else:
            self._cache = None
        self.autofill()
        # Clear simple cache.
        post_save.connect(self.clear, sender=self._model)

    def add_prefix(self, key):
        return "%s%s" % (self._prefix, key)

    def autofill(self):
        if not self._autofill_timeout or not self._cache:
            return
        full_cachekey = self.add_prefix(self._autofill_cachekey)
        if self._cache.get(full_cachekey):
            return
        autofill_values = {}
        autofill_values[full_cachekey] = 1
        for key, value in self.mget(settings.CONFIG.keys()):
            autofill_values[self.add_prefix(key)] = value
        self._cache.set_many(autofill_values, timeout=self._autofill_timeout)

    def mget(self, keys):
        if not keys:
            return
        keys = dict((self.add_prefix(key), key) for key in keys)
        stored = self._model._default_manager.filter(key__in=keys.keys())
        for const in stored:
            yield keys[const.key], const.value

    def get(self, key):
        key = self.add_prefix(key)
        if self._cache:
            value = self._cache.get(key)
        else:
            value = None
        if value is None:
            try:
                value = self._model._default_manager.get(key=key).value
            except self._model.DoesNotExist:
                pass
            else:
                if self._cache:
                    self._cache.add(key, value)
        return value

    def set(self, key, value):
        constance, created = self._model._default_manager.get_or_create(
            key=self.add_prefix(key), defaults={'value': value}
        )
        if not created:
            constance.value = value
            constance.save()

    def clear(self, sender, instance, created, **kwargs):
        if self._cache and not created:
            keys = [self.add_prefix(k)
                    for k in settings.CONFIG.keys()]
            keys.append(self.add_prefix(self._autofill_cachekey))
            self._cache.delete_many(keys)
            self.autofill()
