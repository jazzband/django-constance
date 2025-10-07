from importlib import import_module

from . import LazyConfig
from . import settings

config = LazyConfig()


def import_module_attr(path):
    package, module = path.rsplit(".", 1)
    return getattr(import_module(package), module)


def get_values():
    """
    Get dictionary of values from the backend
    :return:
    """
    # First load a mapping between config name and default value
    default_initial = ((name, options[0]) for name, options in settings.CONFIG.items())
    # Then update the mapping with actually values from the backend
    return dict(default_initial, **dict(config._backend.mget(settings.CONFIG)))


def get_values_for_keys(keys):
    """
    Retrieve values for specified keys from the backend.

    :param keys: List of keys to retrieve.
    :return: Dictionary with values for the specified keys.
    :raises AttributeError: If any key is not found in the configuration.
    """
    if not isinstance(keys, (list, tuple, set)):
        raise TypeError("keys must be a list, tuple, or set of strings")

    # Prepare default initial mapping
    default_initial = {name: options[0] for name, options in settings.CONFIG.items() if name in keys}

    # Check if all keys are present in the default_initial mapping
    missing_keys = [key for key in keys if key not in default_initial]
    if missing_keys:
        raise AttributeError(f'"{", ".join(missing_keys)}" keys not found in configuration.')

    # Merge default values and backend values, prioritizing backend values
    return dict(default_initial, **dict(config._backend.mget(keys)))
