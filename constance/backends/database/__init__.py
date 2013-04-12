from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save
from django.core.cache import get_cache
from django.core.cache.backends.locmem import CacheClass as LocMemCacheClass

from constance.backends import Backend
from constance import settings

db_cache = None
if settings.DATABASE_CACHE_BACKEND:
    db_cache = get_cache(settings.DATABASE_CACHE_BACKEND)
    if isinstance(db_cache, LocMemCacheClass):
        raise ImproperlyConfigured(
            "The CONSTANCE_DATABASE_CACHE_BACKEND setting refers to a "
            "subclass of Django's local-memory backend (%r). Please set "
            "it to a backend that supports cross-process caching."
            % settings.DATABASE_CACHE_BACKEND)


class DatabaseBackend(Backend):
    def __init__(self):
        from constance.backends.database.models import Constance
        self._model = Constance
        self._prefix = settings.DATABASE_PREFIX
        if not self._model._meta.installed:
            raise ImproperlyConfigured(
                "The constance.backends.database app isn't installed "
                "correctly. Make sure it's in your INSTALLED_APPS setting.")
        # Clear simple cache.
        post_save.connect(self.clear, sender=self._model)

    def add_prefix(self, key):
        return "%s%s" % (self._prefix, key)

    def mget(self, keys):
        if not keys:
            return
        keys = dict((self.add_prefix(key), key) for key in keys)
        stored = self._model._default_manager.filter(key__in=keys.keys())
        for const in stored:
            yield keys[const.key], const.value

    def get(self, key):
        key = self.add_prefix(key)
        value = None
        if db_cache:
            value = db_cache.get(key)
        if value is None:
            try:
                value = self._model._default_manager.get(key=key).value
            except self._model.DoesNotExist:
                pass
            else:
                if db_cache:
                    db_cache.add(key, value)
        return value

    def set(self, key, value):
        constance, created = self._model._default_manager.get_or_create(
            key=self.add_prefix(key), defaults={'value': value}
        )
        if not created:
            constance.value = value
            constance.save()

    def clear(self, sender, instance, created, **kwargs):
        if db_cache and not created:
            db_cache.delete_many(settings.CONFIG.keys())
