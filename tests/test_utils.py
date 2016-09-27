# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal

from constance.utils import get_values
from constance.management.commands.constance import _set_constance_value
from django.core.exceptions import ValidationError
from django.test import TransactionTestCase

from constance import config

class UtilsTestCase(TransactionTestCase):

    def test_set_constance_value(self):
        self.assertEqual(config.INT_VALUE, 1)

        _set_constance_value('INT_VALUE', 2)

        self.assertEqual(config.INT_VALUE, 2)

        _set_constance_value('INT_VALUE', '3')

        self.assertEqual(config.INT_VALUE, 3)

    def test_set_constance_value_validation(self):
        self.assertRaises(ValidationError, _set_constance_value, 'INT_VALUE', 'foo')

        _set_constance_value('EMAIL_VALUE', 'a_valid_email@example.com')
        self.assertEqual(config.EMAIL_VALUE, 'a_valid_email@example.com')

        self.assertRaises(ValidationError, _set_constance_value, 'EMAIL_VALUE', 'not a valid email')

    def test_get_get_constance_values(self):

        self.assertEqual(get_values(), {
            'FLOAT_VALUE': 3.1415926536,
            'BOOL_VALUE': True,
            'EMAIL_VALUE': 'test@example.com',
            'INT_VALUE': 1,
            'CHOICE_VALUE': 'yes',
            'TIME_VALUE': datetime.time(23, 59, 59),
            'DATE_VALUE': datetime.date(2010, 12, 24),
            'LINEBREAK_VALUE': 'Spam spam',
            'DECIMAL_VALUE': Decimal('0.1'),
            'STRING_VALUE': 'Hello world',
            'UNICODE_VALUE': u'Rivière-Bonjour',
            'DATETIME_VALUE': datetime.datetime(2010, 8, 23, 11, 29, 24),
            'LONG_VALUE': 123456
        })