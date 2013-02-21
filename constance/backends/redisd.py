import itertools

from django.core.exceptions import ImproperlyConfigured

from constance import settings, utils
from constance.backends import Backend

try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps


class RedisBackend(Backend):

    def __init__(self):
        super(RedisBackend, self).__init__()
        self._prefix = settings.PREFIX
        connection_cls = settings.CONNECTION_CLASS
        if connection_cls is not None:
            self._rd = utils.import_module_attr(connection_cls)()
        else:
            try:
                import redis
            except ImportError:
                raise ImproperlyConfigured(
                    "The Redis backend requires redis-py to be installed.")

            if 'url' in settings.REDIS_CONNECTION:
                self._rd = redis.from_url(settings.REDIS_CONNECTION['url'])
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
        for key, value in itertools.izip(keys, self._rd.mget(prefixed_keys)):
            if value:
                yield key, loads(value)

    def set(self, key, value):
        self._rd.set(self.add_prefix(key), dumps(value))
