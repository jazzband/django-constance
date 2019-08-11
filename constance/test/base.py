"""
Tests override config base entities.
"""
from functools import wraps
from django.test.utils import override_settings

from .. import config


def _setup(override):
    """
    Pre setup handler decorator.
    """
    def decorator_wrapper(func):
        @wraps(func)
        def wrapper(inner_self):
            override.enable()
            func(inner_self)
        return wrapper
    return decorator_wrapper


def _teardown(override):
    """
    Post teardown handler decorator.
    """
    def decorator_wrapper(func):
        @wraps(func)
        def wrapper(inner_self):
            func(inner_self)
            override.disable()
        return wrapper
    return decorator_wrapper


class OverrideConfigBase(override_settings):
    """
    Decorator to modify constance setting for TestCase.

    Based on django.test.utils.override_settings.
    """
    _pre_setup = None
    _post_teardown = None

    def __init__(self, **kwargs):
        super(OverrideConfigBase, self).__init__(**kwargs)
        if not all([self._pre_setup, self._post_teardown]):
            raise Exception("Base override config can not be instantiated.")
        self.original_values = {}

    def __call__(self, test_func):
        """
        Modify the decorated function to override config values.
        """
        if isinstance(test_func, type):
            return self.modify_test_case(test_func)
        else:
            @wraps(test_func)
            def inner(*args, **kwargs):
                with self:
                    return test_func(*args, **kwargs)
        return inner

    def modify_test_case(self, test_case):
        """
        Override the config by modifying TestClass methods.
        """
        original_pre_setup = getattr(test_case, self._pre_setup)
        original_post_teardown = getattr(test_case, self._post_teardown)

        setattr(test_case, self._pre_setup, _setup(self)(original_pre_setup))
        setattr(test_case, self._post_teardown, _teardown(self)(original_post_teardown))

        return test_case

    def enable(self):
        """
        Store original config values and set overridden values.
        """
        # Store the original values to an instance variable
        for config_key in self.options:
            self.original_values[config_key] = getattr(config, config_key)

        # Update config with the overriden values
        self.unpack_values(self.options)

    def disable(self):
        """
        Set original values to the config.
        """
        self.unpack_values(self.original_values)

    @staticmethod
    def unpack_values(options):
        """
        Unpack values from the given dict to config.
        """
        for name, value in options.items():
            setattr(config, name, value)
