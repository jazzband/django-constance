"""
Pytest constance override config plugin.

Inspired by https://github.com/pytest-dev/pytest-django/.
"""
import pytest
from contextlib import ContextDecorator
from constance import config as constance_config
from django.conf import settings


def skip_if_django_not_configured():  # pragma: no cover
    """
    Raises a skip exception if no Django settings are available.
    """
    django_is_configured = bool(os.environ.get("DJANGO_SETTINGS_MODULE"))

    if not django_is_configured and "django.conf" in sys.modules:
        django_is_configured = sys.modules["django.conf"].settings.configured

    if not django_is_configured():
        pytest.skip("no Django settings")


@pytest.hookimpl(trylast=True)
def pytest_configure(config):  # pragma: no cover
    """
    Register override_config marker.
    """
    skip_if_django_not_configured()

    config.addinivalue_line(
        "markers",
        (
            "override_config(**kwargs): "
            "mark test to override django-constance config"
        )
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):  # pragma: no cover
    """
    Validate constance override marker params. Run test with overrided config.
    """
    skip_if_django_not_configured()

    marker = item.get_closest_marker("override_config")
    if marker is not None:
        if marker.args:
            pytest.fail(
                "Constance override can not not accept positional args"
            )
        with override_config(**marker.kwargs):
            yield
    else:
        yield


class override_config(ContextDecorator):
    """
    Override config while running test function.

    Act as context manager and decorator.
    """
    def enable(self):
        """
        Store original config values and set overridden values.
        """
        for key, value in self._to_override.items():
            self._original_values[key] = getattr(constance_config, key)
            setattr(constance_config, key, value)

    def disable(self):
        """
        Set original values to the config.
        """
        for key, value in self._original_values.items():
            setattr(constance_config, key, value)

    def __init__(self, **kwargs):
        self._to_override = kwargs.copy()
        self._original_values = {}

    def __enter__(self):
        skip_if_django_not_configured()

        self.enable()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disable()


@pytest.fixture(name="override_config")
def _override_config():
    """
    Make override_config available as a function fixture.
    """
    skip_if_django_not_configured()

    return override_config
