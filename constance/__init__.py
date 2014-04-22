from constance import utils
from constance import settings

def load_config_class():
    return utils.import_module_attr(settings.CONFIG_CLASS)

config = load_config_class()()
