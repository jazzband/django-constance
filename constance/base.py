from django.core.exceptions import AppRegistryNotReady

from . import settings, utils


def _get_config_class():

    is_ready = False

    class _Config:
        """
        The global config wrapper that handles the backend.
        """

        def init(self):
            super().__setattr__('_backend', utils.import_module_attr(settings.BACKEND)())
            nonlocal is_ready
            is_ready = True

        def __getattr__(self, key):
            if not is_ready:
                raise AppRegistryNotReady("Apps aren't loaded yet.")

            result = self._backend.get(key)
            if result is None:
                result = self._backend.get_default(key)
                return result
            return result

        def __setattr__(self, key, value):
            if not is_ready:
                raise AppRegistryNotReady("Apps aren't loaded yet.")

            if key not in settings.CONFIG:
                raise AttributeError(key)
            self._backend.set(key, value)

        def __dir__(self):
            return settings.CONFIG.keys()

    return _Config


Config = _get_config_class()
