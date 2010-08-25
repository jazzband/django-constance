import os
import redis

try:
    from cPickle import loads, dumps
except ImportError:
    from pickle import loads, dumps

def import_module(path):
    package, module = path.rsplit('.', 1)
    return getattr(__import__(package, None, None, [module]), module)

settings = import_module(os.getenv('CONSTANCE_SETTINGS_MODULE', 'django.conf.settings'))


class Config(object):

    def __init__(self):
        super(Config, self).__setattr__('_prefix', getattr(settings, 'CONSTANCE_PREFIX', 'constance:'))
        try:
            super(Config, self).__setattr__('_rd', import_module(settings.CONSTANCE_CONNECTION_CLASS)())
        except AttributeError:
            super(Config, self).__setattr__('_rd', redis.Redis(**settings.CONSTANCE_CONNECTION))

    def __getattr__(self, key):
        try:
            default, help_text = settings.CONSTANCE_CONFIG[key]
        except KeyError, e:
            raise AttributeError(key)
        result = self._rd.get("%s%s" % (self._prefix, key))
        if result is None:
            result = default
            setattr(self, key, default)
            return result
        return loads(result)

    def __setattr__(self, key, value):
        if key not in settings.CONSTANCE_CONFIG:
            raise AttributeError(key)
        self._rd.set("%s%s" % (self._prefix, key), dumps(value))

    def __dir__(self):
        return settings.CONSTANCE_CONFIG.keys()

