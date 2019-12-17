from . import settings, utils


class Config(object):
    """
    The global config wrapper that handles the backend.
    """
    def __init__(self):
        super(Config, self).__setattr__('_backend',
            utils.import_module_attr(settings.BACKEND)())

    def __getitem__(self, key):
        return self.__getattr__(key)
    
    def __setitem__(self, key, value):
        return self.__setattr__(key, value)

    def __getattr__(self, key):
        try:
            if not len(settings.CONFIG[key]) in (2, 3):
                raise AttributeError(key)
            default = settings.CONFIG[key][0]
        except KeyError:
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
        return settings.CONFIG.keys()
