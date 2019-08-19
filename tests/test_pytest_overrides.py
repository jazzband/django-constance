import pytest

from constance import config
from constance.test.pytest import ConstanceConfigWrapper as override_config


class TestPytestOverrideConfigFunctionDecorator:
    """Test that the override_config decorator works correctly for Pytest classes.

    Test usage of override_config on test method and as context manager.
    """
    def test_default_value_is_true(self):
        """Assert that the default value of config.BOOL_VALUE is True."""
        assert config.BOOL_VALUE

    @pytest.mark.override_config(BOOL_VALUE=False)
    def test_override_config_on_method_changes_config_value(self):
        """Assert that the method decorator changes config.BOOL_VALUE."""
        assert not config.BOOL_VALUE

    def test_override_config_as_context_manager_changes_config_value(self):
        """Assert that the context manager changes config.BOOL_VALUE."""
        with override_config(BOOL_VALUE=False):
            assert not config.BOOL_VALUE

        assert config.BOOL_VALUE


@pytest.mark.override_config(BOOL_VALUE=False)
class TestPytestOverrideConfigClassDecorator:
    """Test that the override_config decorator works on classes."""
    def test_override_config_on_class_changes_config_value(self):
        """Asser that the class decorator changes config.BOOL_VALUE."""
        assert not config.BOOL_VALUE
