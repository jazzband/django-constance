from django.core.exceptions import ImproperlyConfigured
import six

from . import Backend
from .. import settings, utils, signals, config

try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps


class RedisBackend(Backend):

    def __init__(self):
        super(RedisBackend, self).__init__()
        self._prefix = settings.REDIS_PREFIX
        connection_cls = settings.REDIS_CONNECTION_CLASS
        if connection_cls is not None:
            self._rd = utils.import_module_attr(connection_cls)()
        else:
            try:
                import redis
            except ImportError:
                raise ImproperlyConfigured(
                    "The Redis backend requires redis-py to be installed.")
            if isinstance(settings.REDIS_CONNECTION, six.string_types):
                self._rd = redis.from_url(settings.REDIS_CONNECTION)
            else:
                self._rd = redis.Redis(**settings.REDIS_CONNECTION)

    def add_prefix(self, key):
        return "%s%s" % (self._prefix, key)

    def get(self, key):
        value = self._rd.get(self.add_prefix(key))
        if value:
            return loads(value)
        return None

    def mget(self, keys):
        if not keys:
            return
        prefixed_keys = [self.add_prefix(key) for key in keys]
        for key, value in six.moves.zip(keys, self._rd.mget(prefixed_keys)):
            if value:
                yield key, loads(value)

    def set(self, key, value):
        old_value = self.get(key)
        self._rd.set(self.add_prefix(key), dumps(value))
        signals.config_updated.send(
            sender=config, key=key, old_value=old_value, new_value=value
        )
