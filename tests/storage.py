from datetime import datetime, date, time, timedelta
from decimal import Decimal

from constance.base import Config


class StorageTestsMixin:

    def setUp(self):
        self.config = Config()
        super().setUp()

    def test_store(self):
        self.assertEqual(self.config.INT_VALUE, 1)
        self.assertEqual(self.config.BOOL_VALUE, True)
        self.assertEqual(self.config.STRING_VALUE, 'Hello world')
        self.assertEqual(self.config.DECIMAL_VALUE, Decimal('0.1'))
        self.assertEqual(self.config.DATETIME_VALUE, datetime(2010, 8, 23, 11, 29, 24))
        self.assertEqual(self.config.FLOAT_VALUE, 3.1415926536)
        self.assertEqual(self.config.DATE_VALUE, date(2010, 12, 24))
        self.assertEqual(self.config.TIME_VALUE, time(23, 59, 59))
        self.assertEqual(self.config.TIMEDELTA_VALUE, timedelta(days=1, hours=2, minutes=3))
        self.assertEqual(self.config.CHOICE_VALUE, 'yes')
        self.assertEqual(self.config.EMAIL_VALUE, 'test@example.com')

        # set values
        self.config.INT_VALUE = 100
        self.config.BOOL_VALUE = False
        self.config.STRING_VALUE = 'Beware the weeping angel'
        self.config.DECIMAL_VALUE = Decimal('1.2')
        self.config.DATETIME_VALUE = datetime(1977, 10, 2)
        self.config.FLOAT_VALUE = 2.718281845905
        self.config.DATE_VALUE = date(2001, 12, 20)
        self.config.TIME_VALUE = time(1, 59, 0)
        self.config.TIMEDELTA_VALUE = timedelta(days=2, hours=3, minutes=4)
        self.config.CHOICE_VALUE = 'no'
        self.config.EMAIL_VALUE = 'foo@bar.com'

        # read again
        self.assertEqual(self.config.INT_VALUE, 100)
        self.assertEqual(self.config.BOOL_VALUE, False)
        self.assertEqual(self.config.STRING_VALUE, 'Beware the weeping angel')
        self.assertEqual(self.config.DECIMAL_VALUE, Decimal('1.2'))
        self.assertEqual(self.config.DATETIME_VALUE, datetime(1977, 10, 2))
        self.assertEqual(self.config.FLOAT_VALUE, 2.718281845905)
        self.assertEqual(self.config.DATE_VALUE, date(2001, 12, 20))
        self.assertEqual(self.config.TIME_VALUE, time(1, 59, 0))
        self.assertEqual(self.config.TIMEDELTA_VALUE, timedelta(days=2, hours=3, minutes=4))
        self.assertEqual(self.config.CHOICE_VALUE, 'no')
        self.assertEqual(self.config.EMAIL_VALUE, 'foo@bar.com')

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
        self.config.BOOL_VALUE = False
        self.config.DECIMAL_VALUE = Decimal('1.2')
        self.config.DATETIME_VALUE = datetime(1977, 10, 2)
        self.config.DATE_VALUE = date(2001, 12, 20)
        self.config.TIME_VALUE = time(1, 59, 0)

        self.assertEqual(self.config.INT_VALUE, 1)  # this should be the default value
        self.assertEqual(self.config.BOOL_VALUE, False)
        self.assertEqual(self.config.STRING_VALUE, 'Hello world')  # this should be the default value
        self.assertEqual(self.config.DECIMAL_VALUE, Decimal('1.2'))
        self.assertEqual(self.config.DATETIME_VALUE, datetime(1977, 10, 2))
        self.assertEqual(self.config.FLOAT_VALUE, 3.1415926536)  # this should be the default value
        self.assertEqual(self.config.DATE_VALUE, date(2001, 12, 20))
        self.assertEqual(self.config.TIME_VALUE, time(1, 59, 0))
        self.assertEqual(self.config.TIMEDELTA_VALUE, timedelta(days=1, hours=2, minutes=3))
