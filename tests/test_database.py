from django.test import TestCase

from constance import settings
from tests.storage import StorageTestsMixin


class TestDatabase(StorageTestsMixin, TestCase):

    def setUp(self):
        super(TestDatabase, self).setUp()
        self.old_backend = settings.BACKEND
        settings.BACKEND = 'constance.backends.database.DatabaseBackend'

    def tearDown(self):
        settings.BACKEND = self.old_backend
