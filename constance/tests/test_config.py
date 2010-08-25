from django.test import TestCase
from django.conf import settings

from constance import config



class TestStorage(TestCase):

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
