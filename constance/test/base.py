"""
Tests override config base entities.
"""
from functools import wraps
from django.test.utils import override_settings

from .. import config


class OverrideConfigBase(override_settings):
    """
    Decorator to modify constance setting for class or class method during testing session.
    """
    def __init__(self, **kwargs):
        super(OverrideConfigBase, self).__init__(**kwargs)
        self.original_values = {}

    def __call__(self, test_func):
        """
        Modify the decorated method/class to override config values.
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
        Override the config by modifying TestClass setup/teardown methods.
        """
        raise NotImplementedError("%s.modify_test_case is not implemented" % self.__class__.__name__)

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
