# -*- encoding: utf-8 -*-
import sys
from datetime import datetime, date, time
from decimal import Decimal


class StorageTestsMixin(object):

    def test_store(self):
        # read defaults
        del sys.modules['constance']
        from constance import config
        self.assertEquals(config.INT_VALUE, 1)
        self.assertEquals(config.LONG_VALUE, 123456L)
        self.assertEquals(config.BOOL_VALUE, True)
        self.assertEquals(config.STRING_VALUE, 'Hello world')
        self.assertEquals(config.UNICODE_VALUE, u'Rivi\xe8re-Bonjour')
        self.assertEquals(config.DECIMAL_VALUE, Decimal('0.1'))
        self.assertEquals(config.DATETIME_VALUE, datetime(2010, 8, 23, 11, 29, 24))
        self.assertEquals(config.FLOAT_VALUE, 3.1415926536)
        self.assertEquals(config.DATE_VALUE, date(2010, 12, 24))
        self.assertEquals(config.TIME_VALUE, time(23, 59, 59))

        # set values
        config.INT_VALUE = 100
        config.LONG_VALUE = 654321L
        config.BOOL_VALUE = False
        config.STRING_VALUE = 'Beware the weeping angel'
        config.UNICODE_VALUE = 'Québec'.decode('utf-8')
        config.DECIMAL_VALUE = Decimal('1.2')
        config.DATETIME_VALUE = datetime(1977, 10, 2)
        config.FLOAT_VALUE = 2.718281845905
        config.DATE_VALUE = date(2001, 12, 20)
        config.TIME_VALUE = time(1, 59, 0)

        # read again
        self.assertEquals(config.INT_VALUE, 100)
        self.assertEquals(config.LONG_VALUE, 654321L)
        self.assertEquals(config.BOOL_VALUE, False)
        self.assertEquals(config.STRING_VALUE, 'Beware the weeping angel')
        self.assertEquals(config.UNICODE_VALUE, 'Québec'.decode('utf-8'))
        self.assertEquals(config.DECIMAL_VALUE, Decimal('1.2'))
        self.assertEquals(config.DATETIME_VALUE, datetime(1977, 10, 2))
        self.assertEquals(config.FLOAT_VALUE, 2.718281845905)
        self.assertEquals(config.DATE_VALUE, date(2001, 12, 20))
        self.assertEquals(config.TIME_VALUE, time(1, 59, 0))

    def test_nonexistent(self):
        from constance import config
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

    def test_missing_values(self):
        from constance import config

        # set some values and leave out others
        config.LONG_VALUE = 654321L
        config.BOOL_VALUE = False
        config.UNICODE_VALUE = 'Québec'.decode('utf-8')
        config.DECIMAL_VALUE = Decimal('1.2')
        config.DATETIME_VALUE = datetime(1977, 10, 2)
        config.DATE_VALUE = date(2001, 12, 20)
        config.TIME_VALUE = time(1, 59, 0)

        self.assertEquals(config.INT_VALUE, 1)  # this should be the default value
        self.assertEquals(config.LONG_VALUE, 654321L)
        self.assertEquals(config.BOOL_VALUE, False)
        self.assertEquals(config.STRING_VALUE, 'Hello world')  # this should be the default value
        self.assertEquals(config.UNICODE_VALUE, 'Québec'.decode('utf-8'))
        self.assertEquals(config.DECIMAL_VALUE, Decimal('1.2'))
        self.assertEquals(config.DATETIME_VALUE, datetime(1977, 10, 2))
        self.assertEquals(config.FLOAT_VALUE, 3.1415926536)  # this should be the default value
        self.assertEquals(config.DATE_VALUE, date(2001, 12, 20))
        self.assertEquals(config.TIME_VALUE, time(1, 59, 0))
