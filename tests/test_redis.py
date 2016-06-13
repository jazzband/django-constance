from django.test import TestCase

from constance import settings

from tests.storage import StorageTestsMixin


class TestRedis(StorageTestsMixin, TestCase):

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = 'constance.backends.redisd.RedisBackend'
        super(TestRedis, self).setUp()
        self.config._backend._rd.clear()

    def tearDown(self):
        self.config._backend._rd.clear()
        settings.BACKEND = self.old_backend
