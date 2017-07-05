from . import settings, utils


class Config(object):
    """
    The global config wrapper that handles the backend.
    """
    def __init__(self):
        super(Config, self).__setattr__('_backend',
            utils.import_module_attr(settings.BACKEND)())

    def __getattr__(self, key):
        if key in settings.CONFIG_ONLY:
            current_config = settings.CONFIG_ONLY
        else:
            current_config = settings.CONFIG

        try:
            if not len(current_config[key]) in (2, 3):
                raise AttributeError(key)
            default = current_config[key][0]
        except KeyError:
            raise AttributeError(key)
        result = self._backend.get(key)
        if result is None:
            result = default
            setattr(self, key, default)
            return result
        return result

    def __setattr__(self, key, value):
        if key in settings.CONFIG_ONLY:
            self._backend.set(key, value)
        else:
            if key not in settings.CONFIG:
                raise AttributeError(key)
            self._backend.set(key, value)

    def __dir__(self):
        return settings.CONFIG.keys()
