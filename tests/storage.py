# -*- encoding: utf-8 -*-
import sys
import six
from datetime import datetime, date, time
from decimal import Decimal

if six.PY3:
    def long(value):
        return value


class StorageTestsMixin(object):

    def test_store(self):
        # read defaults
        del sys.modules['constance']
        from constance import config
        self.assertEqual(config.INT_VALUE, 1)
        self.assertEqual(config.LONG_VALUE, long(123456))
        self.assertEqual(config.BOOL_VALUE, True)
        self.assertEqual(config.STRING_VALUE, 'Hello world')
        self.assertEqual(config.UNICODE_VALUE, u'Rivi\xe8re-Bonjour')
        self.assertEqual(config.DECIMAL_VALUE, Decimal('0.1'))
        self.assertEqual(config.DATETIME_VALUE, datetime(2010, 8, 23, 11, 29, 24))
        self.assertEqual(config.FLOAT_VALUE, 3.1415926536)
        self.assertEqual(config.DATE_VALUE, date(2010, 12, 24))
        self.assertEqual(config.TIME_VALUE, time(23, 59, 59))

        # set values
        config.INT_VALUE = 100
        config.LONG_VALUE = long(654321)
        config.BOOL_VALUE = False
        config.STRING_VALUE = 'Beware the weeping angel'
        config.UNICODE_VALUE = six.u('Québec')
        config.DECIMAL_VALUE = Decimal('1.2')
        config.DATETIME_VALUE = datetime(1977, 10, 2)
        config.FLOAT_VALUE = 2.718281845905
        config.DATE_VALUE = date(2001, 12, 20)
        config.TIME_VALUE = time(1, 59, 0)

        # read again
        self.assertEqual(config.INT_VALUE, 100)
        self.assertEqual(config.LONG_VALUE, long(654321))
        self.assertEqual(config.BOOL_VALUE, False)
        self.assertEqual(config.STRING_VALUE, 'Beware the weeping angel')
        self.assertEqual(config.UNICODE_VALUE, six.u('Québec'))
        self.assertEqual(config.DECIMAL_VALUE, Decimal('1.2'))
        self.assertEqual(config.DATETIME_VALUE, datetime(1977, 10, 2))
        self.assertEqual(config.FLOAT_VALUE, 2.718281845905)
        self.assertEqual(config.DATE_VALUE, date(2001, 12, 20))
        self.assertEqual(config.TIME_VALUE, time(1, 59, 0))

    def test_nonexistent(self):
        from constance import config
        try:
            config.NON_EXISTENT
        except Exception as e:
            self.assertEqual(type(e), AttributeError)

        try:
            config.NON_EXISTENT = 1
        except Exception as e:
            self.assertEqual(type(e), AttributeError)

    def test_missing_values(self):
        from constance import config

        # set some values and leave out others
        config.LONG_VALUE = long(654321)
        config.BOOL_VALUE = False
        config.UNICODE_VALUE = six.u('Québec')
        config.DECIMAL_VALUE = Decimal('1.2')
        config.DATETIME_VALUE = datetime(1977, 10, 2)
        config.DATE_VALUE = date(2001, 12, 20)
        config.TIME_VALUE = time(1, 59, 0)

        self.assertEqual(config.INT_VALUE, 1)  # this should be the default value
        self.assertEqual(config.LONG_VALUE, long(654321))
        self.assertEqual(config.BOOL_VALUE, False)
        self.assertEqual(config.STRING_VALUE, 'Hello world')  # this should be the default value
        self.assertEqual(config.UNICODE_VALUE, six.u('Québec'))
        self.assertEqual(config.DECIMAL_VALUE, Decimal('1.2'))
        self.assertEqual(config.DATETIME_VALUE, datetime(1977, 10, 2))
        self.assertEqual(config.FLOAT_VALUE, 3.1415926536)  # this should be the default value
        self.assertEqual(config.DATE_VALUE, date(2001, 12, 20))
        self.assertEqual(config.TIME_VALUE, time(1, 59, 0))
