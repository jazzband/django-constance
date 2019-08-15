from django.test import SimpleTestCase

from .base import OverrideConfigBase


__all__ = ["override_config"]


class override_config(OverrideConfigBase):
    """
    UnitTest config override.
    """
    def __init__(self, **kwargs):
        super(override_config, self).__init__(**kwargs)

    def __call__(self, test_func):
        if isinstance(test_func, type):
            if not issubclass(test_func, SimpleTestCase):
                raise Exception(
                    "Only subclasses of Django SimpleTestCase can be "
                    "decorated with override_config")
        return super(override_config, self).__call__(test_func)

    def modify_test_case(self, test_case):
        """
        Override the config by modifying TestCase methods.
        This method follows the Django <= 1.6 method of overriding the
        _pre_setup and _post_teardown hooks rather than modifying the TestCase
        itself.
        """
        original_pre_setup = test_case._pre_setup
        original_post_teardown = test_case._post_teardown

        def _pre_setup(inner_self):
            self.enable()
            original_pre_setup(inner_self)

        def _post_teardown(inner_self):
            original_post_teardown(inner_self)
            self.disable()

        test_case._pre_setup = _pre_setup
        test_case._post_teardown = _post_teardown

        return test_case
