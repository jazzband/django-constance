from constance import settings
from constance.utils import import_module_attr

class Config(object):
    """
    The global config wrapper that handles the backend.
    """
    def __init__(self):
        super(Config, self).__setattr__(
            '_backend', import_module_attr(settings.BACKEND)(settings.PREFIX))

    def __getattr__(self, key):
        try:
            default, help_text = settings.CONFIG[key]
        except KeyError, e:
            raise AttributeError(key)
        result = self._backend.get(key)
        if result is None:
            result = default
            setattr(self, key, default)
            return result
        return result

    def __setattr__(self, key, value):
        if key not in settings.CONFIG:
            raise AttributeError(key)
        self._backend.set(key, value)

    def __dir__(self):
        return settings.CONFIG.iterkeys()
