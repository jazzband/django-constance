import sys

from django.test import TestCase

from constance import settings
from constance.config import Config

from .storage import TestStorage


class TestRedis(TestCase, TestStorage):

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = 'constance.backends.redisd.RedisBackend'
        del sys.modules['constance']
        from constance import config
        config._backend._rd.clear()

    def tearDown(self):
        del sys.modules['constance']
        from constance import config
        config._backend._rd.clear()
        settings.BACKEND = self.old_backend
        import constance
        constance.config = Config()
