# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal

from constance.admin import get_values
from constance.management.commands.constance import _set_constance_value
from django.core.exceptions import ValidationError
from django.test import TestCase


class UtilsTestCase(TestCase):

    def test_set_value_validation(self):
        self.assertRaisesMessage(ValidationError, 'Enter a whole number.', _set_constance_value, 'INT_VALUE', 'foo')
        self.assertRaisesMessage(ValidationError, 'Enter a valid email address.', _set_constance_value, 'EMAIL_VALUE', 'not a valid email')

    def test_get_values(self):

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
