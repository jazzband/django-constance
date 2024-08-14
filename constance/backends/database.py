from django.core.cache import caches
from django.core.cache.backends.locmem import LocMemCache
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError
from django.db import OperationalError
from django.db import ProgrammingError
from django.db import transaction
from django.db.models.signals import post_save

from constance import config
from constance import settings
from constance import signals
from constance.backends import Backend
from constance.codecs import dumps
from constance.codecs import loads


class DatabaseBackend(Backend):
    def __init__(self):
        from constance.models import Constance

        self._model = Constance
        self._prefix = settings.DATABASE_PREFIX
        self._autofill_timeout = settings.DATABASE_CACHE_AUTOFILL_TIMEOUT
        self._autofill_cachekey = 'autofilled'

        if self._model._meta.app_config is None:
            raise ImproperlyConfigured(
                "The constance.backends.database app isn't installed "
                "correctly. Make sure it's in your INSTALLED_APPS setting."
            )

        if settings.DATABASE_CACHE_BACKEND:
            self._cache = caches[settings.DATABASE_CACHE_BACKEND]
            if isinstance(self._cache, LocMemCache):
                raise ImproperlyConfigured(
                    'The CONSTANCE_DATABASE_CACHE_BACKEND setting refers to a '
                    f"subclass of Django's local-memory backend ({settings.DATABASE_CACHE_BACKEND!r}). Please "
                    'set it to a backend that supports cross-process caching.'
                )
        else:
            self._cache = None
        self.autofill()
        # Clear simple cache.
        post_save.connect(self.clear, sender=self._model)

    def add_prefix(self, key):
        return f'{self._prefix}{key}'

    def autofill(self):
        if not self._autofill_timeout or not self._cache:
            return
        full_cachekey = self.add_prefix(self._autofill_cachekey)
        if self._cache.get(full_cachekey):
            return
        autofill_values = {}
        autofill_values[full_cachekey] = 1
        for key, value in self.mget(settings.CONFIG):
            autofill_values[self.add_prefix(key)] = value
        self._cache.set_many(autofill_values, timeout=self._autofill_timeout)

    def mget(self, keys):
        if not keys:
            return
        keys = {self.add_prefix(key): key for key in keys}
        try:
            stored = self._model._default_manager.filter(key__in=keys)
            for const in stored:
                yield keys[const.key], loads(const.value)
        except (OperationalError, ProgrammingError):
            pass

    def get(self, key):
        key = self.add_prefix(key)
        value = None
        if self._cache:
            value = self._cache.get(key)
            if value is None:
                self.autofill()
                value = self._cache.get(key)
        if value is None:
            match = self._model._default_manager.filter(key=key).first()
            if match:
                value = loads(match.value)
                if self._cache:
                    self._cache.add(key, value)
        return value

    def set(self, key, value):
        key = self.add_prefix(key)
        created = False
        queryset = self._model._default_manager.all()
        # Set _for_write attribute as get_or_create method does
        # https://github.com/django/django/blob/2.2.11/django/db/models/query.py#L536
        queryset._for_write = True

        try:
            constance = queryset.get(key=key)
        except (OperationalError, ProgrammingError):
            # database is not created, noop
            return
        except self._model.DoesNotExist:
            try:
                with transaction.atomic(using=queryset.db):
                    queryset.create(key=key, value=dumps(value))
                created = True
            except IntegrityError:
                # Allow concurrent writes
                constance = queryset.get(key=key)

        if not created:
            old_value = loads(constance.value)
            constance.value = dumps(value)
            constance.save(update_fields=['value'])
        else:
            old_value = None

        if self._cache:
            self._cache.set(key, value)

        signals.config_updated.send(sender=config, key=key, old_value=old_value, new_value=value)

    def clear(self, sender, instance, created, **kwargs):
        if self._cache and not created:
            keys = [self.add_prefix(k) for k in settings.CONFIG]
            keys.append(self.add_prefix(self._autofill_cachekey))
            self._cache.delete_many(keys)
            self.autofill()
