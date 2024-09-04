from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from decimal import Decimal

from constance import settings
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
        self.assertEqual(self.config.LIST_VALUE, [1, '1', date(2019, 1, 1)])
        self.assertEqual(
            self.config.JSON_VALUE,
            {
                'key': 'value',
                'key2': 2,
                'key3': [1, 2, 3],
                'key4': {'key': 'value'},
                'key5': date(2019, 1, 1),
                'key6': None,
            },
        )

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
        self.config.LIST_VALUE = [1, date(2020, 2, 2)]
        self.config.JSON_VALUE = {'key': 'OK'}

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
        self.assertEqual(self.config.LIST_VALUE, [1, date(2020, 2, 2)])
        self.assertEqual(self.config.JSON_VALUE, {'key': 'OK'})

    def test_nonexistent(self):
        self.assertRaises(AttributeError, getattr, self.config, 'NON_EXISTENT')

        with self.assertRaises(AttributeError):
            self.config.NON_EXISTENT = 1

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

    def test_backend_retrieves_multiple_values(self):
        # Check corner cases such as falsy values
        self.config.INT_VALUE = 0
        self.config.BOOL_VALUE = False
        self.config.STRING_VALUE = ''

        values = dict(self.config._backend.mget(settings.CONFIG))
        self.assertEqual(values['INT_VALUE'], 0)
        self.assertEqual(values['BOOL_VALUE'], False)
        self.assertEqual(values['STRING_VALUE'], '')

    def test_backend_does_not_return_none_values(self):
        result = dict(self.config._backend.mget(settings.CONFIG))
        self.assertEqual(result, {})
