from datetime import datetime
from decimal import Decimal

from django.test import TestCase
from django.conf import settings

from constance import config



class TestStorage(TestCase):

    def tearDown(self):
        config._rd.clear()

    def test_store(self):
        # read defaults
        self.assertEquals(config.INT_VALUE, 1)
        self.assertEquals(config.BOOL_VALUE, True)
        self.assertEquals(config.STRING_VALUE, 'Hello world')
        self.assertEquals(config.DECIMAL_VALUE, Decimal('0.1'))
        self.assertEquals(config.DATETIME_VALUE, datetime(2010, 8, 23, 11, 29, 24))
        self.assertEquals(config.FLOAT_VALUE, 3.1415926536)

        # set values
        config.INT_VALUE = 100
        config.BOOL_VALUE = False
        config.STRING_VALUE = 'Beware the weeping angel'
        config.DECIMAL_VALUE = Decimal('1.2')
        config.DATETIME_VALUE = datetime(1977, 10, 2)
        config.FLOAT_VALUE = 2.718281845905

        # read again
        self.assertEquals(config.INT_VALUE, 100)
        self.assertEquals(config.BOOL_VALUE, False)
        self.assertEquals(config.STRING_VALUE, 'Beware the weeping angel')
        self.assertEquals(config.DECIMAL_VALUE, Decimal('1.2'))
        self.assertEquals(config.DATETIME_VALUE, datetime(1977, 10, 2))
        self.assertEquals(config.FLOAT_VALUE, 2.718281845905)

    def test_nonexistent(self):
        try:
            config.NON_EXISTENT
        except Exception, e:
            pass
        self.assertEquals(type(e), AttributeError)

        try:
            config.NON_EXISTENT = 1
        except Exception, e:
            pass
        self.assertEquals(type(e), AttributeError)
