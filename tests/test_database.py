from django.test import TestCase

from constance import settings
from tests.storage import StorageTestsMixin


class TestDatabase(StorageTestsMixin, TestCase):

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = 'constance.backends.database.DatabaseBackend'
        super(TestDatabase, self).setUp()

    def tearDown(self):
        settings.BACKEND = self.old_backend
