import six
from django.utils.datastructures import SortedDict
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

CONFIGURATION_ERROR = ("Constance configuration key '%s' must have either a "
                       "2-tuple with default value and help text or a dictionary "
                       "with at least the 'default' and 'help_text' set.")


def import_module_attr(path):
    package, module = path.rsplit('.', 1)
    return getattr(import_module(package), module)


def parse_config(config):
    """ Parse Constance configuration dictionary

    Checks if mandatory keywords are set and provides backwards compatibility
    for (default, help_text) tuple based CONSTANCE_CONFIG.
    """
    if not config:
        return config

    cfg = SortedDict()
    for key, value in six.iteritems(config):
        if isinstance(value, (tuple, list)):
            if len(value) == 2:
                default, help_text = value
                cfg[key] = {
                    'default': default,
                    'help_text': help_text,
                }
                continue
        elif isinstance(value, dict):
            if 'default' in value and 'help_text' in value:
                cfg[key] = value
                continue
        raise ImproperlyConfigured(CONFIGURATION_ERROR % (key, ))
    return cfg
