import sys

from django.test import TestCase

import constance
from constance import settings
from constance.config import Config

from tests.storage import StorageTestsMixin


class TestDatabase(TestCase, StorageTestsMixin):

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = 'constance.backends.database.DatabaseBackend'

    def tearDown(self):
        settings.BACKEND = self.old_backend
        constance.config = constance.load_config_class()()
