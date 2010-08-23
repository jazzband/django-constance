import redis

from django.conf import settings
from django.utils.importlib import import_module



class Config(object):

    def __init__(self):
        try:
            module, class_ = settings.CONSTANCE_CONNECTION_CLASS.rsplit('.')
            self._rd = getattr(import_module(module), class_)()
        except AttributeError:
            self._rd = redis.Redis(**settings.CONSTANCE_CONNECTION)

    def __getattr__(self, key):
        if key.startswith('_'):
            return super(Config, self).__getattr__(key, value)
        default, decode, help_text = settings.CONSTANCE_CONFIG[key]
        result = self._rd.get("%s%s" % (self.prefix, key))
        if result is None:
            result = default
            setattr(self, key, default)
        return decode(result)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            return super(Config, self).__setattr__(key, value)
        self._rd.set("%s%s" % (self.prefix, key), value)

