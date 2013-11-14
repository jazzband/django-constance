from constance.config import Config
from constance import utils
from constance import settings

config = utils.import_module_attr(settings.CONFIG_CLASS)()
