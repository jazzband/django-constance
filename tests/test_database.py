import sys

from django.test import TestCase

from constance import settings
from constance.config import Config

from .storage import TestStorage


class TestDatabase(TestCase, TestStorage):

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = 'constance.backends.database.DatabaseBackend'

    def tearDown(self):
        del sys.modules['constance']
        settings.BACKEND = self.old_backend
        import constance
        constance.config = Config()
