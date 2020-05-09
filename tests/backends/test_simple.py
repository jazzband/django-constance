from django.test import TestCase

from constance import settings

from tests.storage import StorageTestsMixin


class TestSimple(StorageTestsMixin, TestCase):

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = 'constance.backends.simple.SimpleBackend'
        super().setUp()
        self.config._backend._storage = {}

    def tearDown(self):
        self.config._backend._storage = {}
        settings.BACKEND = self.old_backend
