import redis

from django.conf import settings
from django.utils.importlib import import_module



class Config(object):

    def __init__(self):
        try:
            module, class_ = settings.CONSTANCE_CONNECTION_CLASS.rsplit('.')
            self.rd = getattr(import_module(module), class_)()
        except AttributeError:
            self.rd = redis.Redis(**settings.CONSTANCE_CONNECTION)
        self.rd = connection

    def __getattr__(self, key):
        default, decode, help_text = settings.CONSTANCE_CONFIG[key]
        result = self.rd.get("%s%s" % (self.prefix, key))
        if result is None:
            result = default
            setattr(self, key, default)
        return decode(result)

    def __setattr__(self, key, value):
        self.rd.set("%s%s" % (self.prefix, key), value)

