from django.test import SimpleTestCase

from .base import OverrideConfigBase

__all__ = ["override_config"]


class override_config(OverrideConfigBase):
    """
    UnitTest config override.

    This override follows the Django <= 1.6 method of overriding the
    _pre_setup and _post_teardown hooks rather than modifying the TestCase
    itself.
    """
    _pre_setup = "_pre_setup"
    _post_teardown = "_post_teardown"

    def __call__(self, test_func):
        if isinstance(test_func, type):
            if not issubclass(test_func, SimpleTestCase):
                raise Exception(
                    "Only subclasses of Django SimpleTestCase can be "
                    "decorated with override_config")
        return super(override_config, self).__call__(test_func)
