import sys

from django.test import TestCase

from constance import settings
from constance.config import Config

from tests.storage import StorageTestsMixin


class TestRedis(TestCase, StorageTestsMixin):

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = 'constance.backends.redisd.RedisBackend'
        from constance import config
        config._backend._rd.clear()

    def tearDown(self):
        from constance import config
        config._backend._rd.clear()
        settings.BACKEND = self.old_backend
        import constance
        constance.config = constance.load_config_class()()
