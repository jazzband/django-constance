import redis

from django.conf import settings
from django.utils.importlib import import_module



class Config(object):

    def __init__(self):
        super(Config, self).__setattr__('_prefix', getattr(settings.CONSTANCE_PREFIX, 'constance:')
        try:
            module, class_ = settings.CONSTANCE_CONNECTION_CLASS.rsplit('.')
            super(Config, self).__setattr__('_rd', getattr(import_module(module), class_)())
        except AttributeError:
            super(Config, self).__setattr__('_rd', redis.Redis(**settings.CONSTANCE_CONNECTION))

    def __getattr__(self, key):
        default, decode, help_text = settings.CONSTANCE_CONFIG[key]
        result = self._rd.get("%s%s" % (self._prefix, key))
        if result is None:
            result = default
            setattr(self, key, default)
        return decode(result)

    def __setattr__(self, key, value):
        self._rd.set("%s%s" % (self._prefix, key), value)

