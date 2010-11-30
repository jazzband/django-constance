from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save
from django.utils.functional import memoize

from constance import settings
from constance.utils import import_module_attr

try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps


class Backend(object):

    def __init__(self, prefix):
        self._prefix = prefix

    def get(self, key):
        """
        Get the key from the backend store and return it.
        Return None if not found.
        """
        raise NotImplementedError

    def set(self, key, value):
        """
        Add the value to the backend store given the key.
        """
        raise NotImplementedError

db_cache = {}

class DatabaseBackend(Backend):

    def __init__(self, prefix):
        super(DatabaseBackend, self).__init__(prefix)
        from constance.models import Constance
        if not Constance._meta.installed:
            raise ImproperlyConfigured(
                "The constance app isn't installed correctly. "
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

class RedisBackend(Backend):

    def __init__(self, prefix):
        super(RedisBackend, self).__init__(prefix)
        connection_cls = settings.CONNECTION_CLASS
        if connection_cls is not None:
            self._rd = import_module_attr(connection_cls)()
        else:
            import redis
            self._rd = redis.Redis(**settings.REDIS_CONNECTION)

    def get(self, key):
        value = self._rd.get("%s%s" % (self._prefix, key))
        if value:
            return loads(value)
        return None

    def set(self, key, value):
        self._rd.set("%s%s" % (self._prefix, key), dumps(value))

