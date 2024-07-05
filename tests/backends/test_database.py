from django.test import TestCase

from constance import settings
from tests.storage import StorageTestsMixin


class TestDatabase(StorageTestsMixin, TestCase):
    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = 'constance.backends.database.DatabaseBackend'
        super().setUp()

    def test_database_queries(self):
        # Read and set to default value
        with self.assertNumQueries(5):
            self.assertEqual(self.config.INT_VALUE, 1)

        # Read again
        with self.assertNumQueries(1):
            self.assertEqual(self.config.INT_VALUE, 1)

        # Set value
        with self.assertNumQueries(2):
            self.config.INT_VALUE = 15

    def tearDown(self):
        settings.BACKEND = self.old_backend
