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
            self.config.INT_VALUE

        # Read again
        with self.assertNumQueries(1):
            self.config.INT_VALUE

        # Set value
        with self.assertNumQueries(2):
            self.config.INT_VALUE = 15

    def tearDown(self):
        settings.BACKEND = self.old_backend


class TestCachingDatabase(StorageTestsMixin, TestCase):
    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = 'constance.backends.database.CachingDatabaseBackend'
        super().setUp()

    def tearDown(self):
        settings.BACKEND = self.old_backend

    def test_database_queries(self):
        # Read and set to default value
        with self.assertNumQueries(5):
            for _ in range(100):
                self.config.INT_VALUE

        # Read again
        with self.assertNumQueries(0):
            for _ in range(100):
                self.config.INT_VALUE

        # Set value and local read
        with self.assertNumQueries(2):
            self.config.INT_VALUE = 15
            for _ in range(100):
                self.config.INT_VALUE