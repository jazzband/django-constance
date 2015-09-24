try:
    # available in Python 2.7+
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module


def import_module_attr(path):
    package, module = path.rsplit('.', 1)
    return getattr(import_module(package), module)
