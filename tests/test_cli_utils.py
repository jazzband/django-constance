# -*- coding: utf-8 -*-

from constance_cli.utils import get_constance_value, set_constance_value
from django.core.exceptions import ValidationError
from django.test import TransactionTestCase


class UtilsTestCase(TransactionTestCase):
    def test_get_constance_value(self):
        self.assertEqual(get_constance_value('INT_VALUE'), 1)
        self.assertEqual(get_constance_value('STRING_VALUE'), 'Hello world', 'greetings')

    def test_set_constance_value(self):
        self.assertEqual(get_constance_value('INT_VALUE'), 1)

        set_constance_value('INT_VALUE', 2)

        self.assertEqual(get_constance_value('INT_VALUE'), 2)

        set_constance_value('INT_VALUE', '3')

        self.assertEqual(get_constance_value('INT_VALUE'), 3)

    def test_set_constance_value_validation(self):
        self.assertRaises(ValidationError, set_constance_value, 'INT_VALUE', 'foo')

        set_constance_value('EMAIL_VALUE', 'a_valid_email@example.com')
        self.assertEqual(get_constance_value('EMAIL_VALUE'), 'a_valid_email@example.com')

        self.assertRaises(ValidationError, set_constance_value, 'EMAIL_VALUE', 'not a valid email')
