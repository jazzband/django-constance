from django.test import TestCase

from constance import settings
from tests.storage import StorageTestsMixin


class TestRedis(StorageTestsMixin, TestCase):
    _BACKEND = 'constance.backends.redisd.RedisBackend'

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = self._BACKEND
        super().setUp()
        self.config._backend._rd.clear()

    def tearDown(self):
        self.config._backend._rd.clear()
        settings.BACKEND = self.old_backend


class TestCachingRedis(TestRedis):
    _BACKEND = 'constance.backends.redisd.CachingRedisBackend'
