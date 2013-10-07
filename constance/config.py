from constance import settings, utils


class Config(object):
    """
    The global config wrapper that handles the backend.
    """
    def __init__(self):
        super(Config, self).__setattr__('_backend',
            utils.import_module_attr(settings.BACKEND)())
        if settings.RETRIEVE_ALL_KEYS:
            super(Config, self).__setattr__('_keys',{})

    def __getattr__(self, key):
        if settings.RETRIEVE_ALL_KEYS and self._keys:
            for key,value in self._backend.mget(settings.CONFIG.keys()):
                self._keys[key] = value
        try:
            default, help_text = settings.CONFIG[key]
        except KeyError:
            raise AttributeError(key)
        if settings.RETRIEVE_ALL_KEYS:
            result = self._keys.get(key)
        else:
            result = self._backend.get(key)
        if result is None:
            result = default
            setattr(self, key, default)
            return result
        return result

    def __setattr__(self, key, value):
        if key not in settings.CONFIG:
            raise AttributeError(key)
        if settings.RETRIEVE_ALL_KEYS:
            self._keys[key] = value
        self._backend.set(key, value)

    def __dir__(self):
        return settings.CONFIG.keys()

