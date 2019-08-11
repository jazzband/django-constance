from .base import OverrideConfigBase


__all__ = ["override_config"]


class override_config(OverrideConfigBase):
    """
    Pytest config override.
    """
    _pre_setup = "setup"
    _post_teardown = "teardown"
