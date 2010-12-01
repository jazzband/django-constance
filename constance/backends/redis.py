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
            import redis
            self._rd = redis.Redis(**settings.REDIS_CONNECTION)

    def get(self, key):
        value = self._rd.get("%s%s" % (self._prefix, key))
        if value:
            return loads(value)
        return None

    def set(self, key, value):
        self._rd.set("%s%s" % (self._prefix, key), dumps(value))
