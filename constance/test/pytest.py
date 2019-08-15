import pytest
from .base import OverrideConfigBase


__all__ = ["override_config"]


class override_config(OverrideConfigBase):
    """
    Pytest config override.
    """
    def modify_test_case(self, test_case):
        """
        Override the config by injecting a hidden autouse, class scoped fixture
        into the collected class object.

        Respects setup_class/teardown_class.
        """
        @pytest.fixture(autouse=True, scope="class")
        def _setup_class_fixture():
            self.enable()
            yield
            self.disable()

        test_case.__pytest_setup_class = _setup_class_fixture
        return test_case
