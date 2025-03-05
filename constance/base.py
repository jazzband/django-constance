from . import settings
from . import utils
import importlib


def get_function_from_string(path):
    module_path, function_name = path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    return getattr(module, function_name)

class Config:
    """The global config wrapper that handles the backend."""

    def __init__(self):
        super().__setattr__('_backend', utils.import_module_attr(settings.BACKEND)())

    def __getattr__(self, key):
        try:
            config_value = settings.CONFIG[key]
            if len(config_value) not in (2, 3):
                raise AttributeError(key)
            default = config_value[0]
            derived = len(config_value) == 3 and config_value[2] == 'derived_value'
        except KeyError as e:
            raise AttributeError(key) from e

        if derived:
            if isinstance(default, str):
                default = get_function_from_string(default)
            assert callable(default), "derived_value must have a callable default value"
            return default(self)
        
        result = self._backend.get(key)
        if result is None:
            result = default
            setattr(self, key, default)
            return result
        return result

    def __setattr__(self, key, value):
        if key not in settings.CONFIG:
            raise AttributeError(key)
        if len(settings.CONFIG[key]) == 3 and settings.CONFIG[key][2] == 'derived_value':
            raise AttributeError(key)
        self._backend.set(key, value)

    def __dir__(self):
        return settings.CONFIG.keys()
