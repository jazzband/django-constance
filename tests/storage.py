# -*- encoding: utf-8 -*-
from datetime import datetime, date, time
from decimal import Decimal
from django.utils import six

if six.PY3:
    def long(value):
        return value

from constance.base import Config


class StorageTestsMixin(object):

    def setUp(self):
        self.config = Config()
        super(StorageTestsMixin, self).setUp()

    def test_store(self):
        self.assertEqual(self.config.INT_VALUE, 1)
        self.assertEqual(self.config.LONG_VALUE, long(123456))
        self.assertEqual(self.config.BOOL_VALUE, True)
        self.assertEqual(self.config.STRING_VALUE, 'Hello world')
        self.assertEqual(self.config.UNICODE_VALUE, six.u('Rivière-Bonjour'))
        self.assertEqual(self.config.DECIMAL_VALUE, Decimal('0.1'))
        self.assertEqual(self.config.DATETIME_VALUE, datetime(2010, 8, 23, 11, 29, 24))
        self.assertEqual(self.config.FLOAT_VALUE, 3.1415926536)
        self.assertEqual(self.config.DATE_VALUE, date(2010, 12, 24))
        self.assertEqual(self.config.TIME_VALUE, time(23, 59, 59))
        self.assertEqual(self.config.CHOICE_VALUE, 'yes')

        # set values
        self.config.INT_VALUE = 100
        self.config.LONG_VALUE = long(654321)
        self.config.BOOL_VALUE = False
        self.config.STRING_VALUE = 'Beware the weeping angel'
        self.config.UNICODE_VALUE = six.u('Québec')
        self.config.DECIMAL_VALUE = Decimal('1.2')
        self.config.DATETIME_VALUE = datetime(1977, 10, 2)
        self.config.FLOAT_VALUE = 2.718281845905
        self.config.DATE_VALUE = date(2001, 12, 20)
        self.config.TIME_VALUE = time(1, 59, 0)
        self.config.CHOICE_VALUE = 'no'

        # read again
        self.assertEqual(self.config.INT_VALUE, 100)
        self.assertEqual(self.config.LONG_VALUE, long(654321))
        self.assertEqual(self.config.BOOL_VALUE, False)
        self.assertEqual(self.config.STRING_VALUE, 'Beware the weeping angel')
        self.assertEqual(self.config.UNICODE_VALUE, six.u('Québec'))
        self.assertEqual(self.config.DECIMAL_VALUE, Decimal('1.2'))
        self.assertEqual(self.config.DATETIME_VALUE, datetime(1977, 10, 2))
        self.assertEqual(self.config.FLOAT_VALUE, 2.718281845905)
        self.assertEqual(self.config.DATE_VALUE, date(2001, 12, 20))
        self.assertEqual(self.config.TIME_VALUE, time(1, 59, 0))
        self.assertEqual(self.config.CHOICE_VALUE, 'no')

    def test_nonexistent(self):
        try:
            self.config.NON_EXISTENT
        except Exception as e:
            self.assertEqual(type(e), AttributeError)

        try:
            self.config.NON_EXISTENT = 1
        except Exception as e:
            self.assertEqual(type(e), AttributeError)

    def test_missing_values(self):
        # set some values and leave out others
        self.config.LONG_VALUE = long(654321)
        self.config.BOOL_VALUE = False
        self.config.UNICODE_VALUE = six.u('Québec')
        self.config.DECIMAL_VALUE = Decimal('1.2')
        self.config.DATETIME_VALUE = datetime(1977, 10, 2)
        self.config.DATE_VALUE = date(2001, 12, 20)
        self.config.TIME_VALUE = time(1, 59, 0)

        self.assertEqual(self.config.INT_VALUE, 1)  # this should be the default value
        self.assertEqual(self.config.LONG_VALUE, long(654321))
        self.assertEqual(self.config.BOOL_VALUE, False)
        self.assertEqual(self.config.STRING_VALUE, 'Hello world')  # this should be the default value
        self.assertEqual(self.config.UNICODE_VALUE, six.u('Québec'))
        self.assertEqual(self.config.DECIMAL_VALUE, Decimal('1.2'))
        self.assertEqual(self.config.DATETIME_VALUE, datetime(1977, 10, 2))
        self.assertEqual(self.config.FLOAT_VALUE, 3.1415926536)  # this should be the default value
        self.assertEqual(self.config.DATE_VALUE, date(2001, 12, 20))
        self.assertEqual(self.config.TIME_VALUE, time(1, 59, 0))
