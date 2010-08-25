from django.test import TestCase
from django.conf import settings

from constance import config



class TestStorage(TestCase):

    def setUp(self):
        self.old_config = getattr(settings, 'CONSTANCE_CONFIG', None)
        settings.CONSTANCE_CONFIG = {
            'INT_VALUE': (1, 'some int'),
            'BOOL_VALUE': (True, 'true or false'),
            'STRING_VALUE': ('Hello world', 'greetings'),
        }

    def test_store(self):
        # read defaults
        self.assertEquals(config.INT_VALUE, 1)
        self.assertEquals(config.BOOL_VALUE, True)
        self.assertEquals(config.STRING_VALUE, 'Hello world')

        config.INT_VALUE = 100
        config.BOOL_VALUE = False

        self.assertEquals(config.INT_VALUE, 100)
        self.assertEquals(config.BOOL_VALUE, False)
        self.assertEquals(config.STRING_VALUE, 'Hello world')

    def tearDown(self):
        if self.old_config:
            settings.CONSTANCE_CONFIG = self.old_config
