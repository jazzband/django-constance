from importlib import import_module


from constance import config
from . import settings


def import_module_attr(path):
    package, module = path.rsplit('.', 1)
    return getattr(import_module(package), module)


def get_values():
    """
    Get dictionary of values from the backend
    """

    # First load a mapping between config name and default value
    default_initial = ((name, options[0])
                       for name, options in settings.CONFIG.items())
    # Then update the mapping with actually values from the backend
    initial = dict(default_initial, **dict(config._backend.mget(settings.CONFIG)))

    return initial
