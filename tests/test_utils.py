# -*- coding: utf-8 -*-

from constance.forms import set_constance_value
from django.core.exceptions import ValidationError
from django.test import TransactionTestCase

from constance import config

class UtilsTestCase(TransactionTestCase):

    def test_set_constance_value(self):
        self.assertEqual(config.INT_VALUE, 1)

        set_constance_value('INT_VALUE', 2)

        self.assertEqual(config.INT_VALUE, 2)

        set_constance_value('INT_VALUE', '3')

        self.assertEqual(config.INT_VALUE, 3)

    def test_set_constance_value_validation(self):
        self.assertRaises(ValidationError, set_constance_value, 'INT_VALUE', 'foo')

        set_constance_value('EMAIL_VALUE', 'a_valid_email@example.com')
        self.assertEqual(config.EMAIL_VALUE, 'a_valid_email@example.com')

        self.assertRaises(ValidationError, set_constance_value, 'EMAIL_VALUE', 'not a valid email')
