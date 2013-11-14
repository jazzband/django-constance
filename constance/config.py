import time
from constance import settings, utils


class Config(object):
    """
    The global config wrapper that handles the backend.
    """
    def __init__(self):
        super(Config, self).__setattr__('_backend',
            utils.import_module_attr(settings.BACKEND)())

    def __getattr__(self, key):
        try:
            opts = settings.CONFIG[key]
        except KeyError:
            raise AttributeError(key)
        else:
            default = opts['default']
            help_text = opts['help_text']
        result = self._backend.get(key)
        if result is None:
            result = default
            if not settings.READONLY:
                setattr(self, key, default)
            return result
        return result

    def __setattr__(self, key, value):
        if key not in settings.CONFIG:
            raise AttributeError(key)
        self._backend.set(key, value)

    def __dir__(self):
        return settings.CONFIG.keys()


class CachedConfig(Config):
    """
    Cached version of config

    Cached the resulting config value for CACHE_TIMEOUT seconds.
    """

    def __init__(self):
        super(CachedConfig, self).__init__()
        super(Config, self).__setattr__('_cache', {})

    def __getattr__(self, key):
        try:
            expire, value = self._cache[key]
            if expire > time.time():
                return value
        except KeyError:
            pass

        # if key does not exist in _cache or is expired, retreive it from the backend
        value = super(CachedConfig, self).__getattr__(key)
        expire = time.time() + settings.CACHE_TIMEOUT
        self._cache[key] = (expire, value)
        return value

    def __setattr__(self, key, value):
        super(CachedConfig, self).__setattr__(key, value)
        expire = time.time() + settings.CACHE_TIMEOUT
        self._cache[key] = (expire, value)


class CachedAllConfig(Config):
    """
    Cached version of config that caches all config key, value pairs at once

    Cached all the config values for CACHE_TIMEOUT seconds.
    This has the benefit of being able to do mget() to retreiving the values
    lowering the overhead of retreiving the values. Drawback is that if only a
    few keys are used it will actually cause an additional overhead retreiving
    values which will not be accessed most of the time within the CACHE_TIMEOUT
    period.
    """

    def __init__(self):
        super(CachedAllConfig, self).__init__()
        super(Config, self).__setattr__('_cache', {})
        super(Config, self).__setattr__('_expired', 0)

    def refresh_cache(self):
        self._cache.update(dict((k, v['default']) for k, v in settings.CONFIG.iteritems()))
        self._cache.update(dict(self._backend.mget(settings.CONFIG.iterkeys())))
        super(Config, self).__setattr__('_expired', time.time() + settings.CACHE_TIMEOUT)

    def __getattr__(self, key):
        if self._expired < time.time():
            self.refresh_cache()

        try:
            value = self._cache[key]
        except KeyError:
            pass

        # if key does not exist in _cache, retreive it from the backend
        value = super(CachedAllConfig, self).__getattr__(key)
        self._cache[key] = value
        return value

    def __setattr__(self, key, value):
        super(CachedAllConfig, self).__setattr__(key, value)
        self._cache[key] = value
