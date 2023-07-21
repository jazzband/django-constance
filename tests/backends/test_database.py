from unittest.mock import MagicMock

from django.db.utils import OperationalError, ProgrammingError
from django.test import TestCase

from constance import settings
from constance.backends.database import DatabaseBackend
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

    def test_model_does_not_exist_error_does_not_raise(self):
        backend = DatabaseBackend()
        original_get = backend._model._default_manager.get
        backend._model._default_manager.get = MagicMock(side_effect=backend._model.DoesNotExist)
        self.assertIsNone(backend.get('does_not_exist'))
        backend._model._default_manager.get = original_get

    def test_operational_error_is_raised(self):
        backend = DatabaseBackend()
        original_get = backend._model._default_manager.get
        backend._model._default_manager.get = MagicMock(side_effect=OperationalError)
        self.assertRaises(OperationalError, backend.get, 'does_not_exist')
        backend._model._default_manager.get = original_get

    def test_programming_error_does_not_raise(self):
        backend = DatabaseBackend()
        original_get = backend._model._default_manager.get
        backend._model._default_manager.get = MagicMock(side_effect=ProgrammingError)
        self.assertIsNone(backend.get('does_not_exist'))
        backend._model._default_manager.get = original_get

    def tearDown(self):
        settings.BACKEND = self.old_backend
