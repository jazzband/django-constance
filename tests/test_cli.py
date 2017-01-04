# -*- coding: utf-8 -*-

from datetime import datetime
from textwrap import dedent

from django.core.management import call_command, CommandError
from django.test import TransactionTestCase
from django.utils.encoding import smart_str
from django.utils.six import StringIO

from constance import config


class CliTestCase(TransactionTestCase):
    def setUp(self):
        self.out = StringIO()

    def test_help(self):
        try:
            call_command('constance', '--help')
        except SystemExit:
            pass

    def test_list(self):
        call_command('constance', 'list', stdout=self.out)

        self.assertEqual(set(self.out.getvalue().splitlines()), set(dedent(smart_str(
u"""        BOOL_VALUE	True
        EMAIL_VALUE	test@example.com
        INT_VALUE	1
        LINEBREAK_VALUE	Spam spam
        DATE_VALUE	2010-12-24
        TIME_VALUE	23:59:59
        LONG_VALUE	123456
        STRING_VALUE	Hello world
        UNICODE_VALUE	Rivière-Bonjour
        CHOICE_VALUE	yes
        DECIMAL_VALUE	0.1
        DATETIME_VALUE	2010-08-23 11:29:24
        FLOAT_VALUE	3.1415926536
""")).splitlines()))

    def test_get(self):
        call_command('constance', *('get EMAIL_VALUE'.split()), stdout=self.out)

        self.assertEqual(self.out.getvalue().strip(), "test@example.com")

    def test_set(self):
        call_command('constance', *('set EMAIL_VALUE blah@example.com'.split()), stdout=self.out)

        self.assertEqual(config.EMAIL_VALUE, "blah@example.com")

        call_command('constance', *('set', 'DATETIME_VALUE', '2011-09-24', '12:30:25'), stdout=self.out)

        self.assertEqual(config.DATETIME_VALUE, datetime(2011, 9, 24, 12, 30, 25))

    def test_get_invalid_name(self):
        self.assertRaisesMessage(CommandError, "NOT_A_REAL_CONFIG is not defined in settings.CONSTANCE_CONFIG",
                                 call_command, 'constance', 'get', 'NOT_A_REAL_CONFIG')

    def test_set_invalid_name(self):
        self.assertRaisesMessage(CommandError, "NOT_A_REAL_CONFIG is not defined in settings.CONSTANCE_CONFIG",
                                 call_command, 'constance', 'set', 'NOT_A_REAL_CONFIG', 'foo')

    def test_set_invalid_value(self):
        self.assertRaisesMessage(CommandError, "Enter a valid email address.",
                                 call_command, 'constance', 'set', 'EMAIL_VALUE', 'not a valid email')

    def test_set_invalid_multi_value(self):
        self.assertRaisesMessage(CommandError, "Enter a list of values.",
                                 call_command, 'constance', 'set', 'DATETIME_VALUE', '2011-09-24 12:30:25')
