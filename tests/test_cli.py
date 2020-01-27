from datetime import datetime
from textwrap import dedent

from django.apps import apps
from django.conf import settings
from django.core.management import call_command, CommandError
from django.test import TransactionTestCase
from django.utils import timezone
from django.utils.encoding import smart_str
from io import StringIO

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
"""        BOOL_VALUE	True
        EMAIL_VALUE	test@example.com
        INT_VALUE	1
        LINEBREAK_VALUE	Spam spam
        DATE_VALUE	2010-12-24
        TIME_VALUE	23:59:59
        TIMEDELTA_VALUE	1 day, 2:03:00
        STRING_VALUE	Hello world
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

        expected = datetime(2011, 9, 24, 12, 30, 25)
        if settings.USE_TZ:
            expected = timezone.make_aware(expected)
        self.assertEqual(config.DATETIME_VALUE, expected)

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

    def test_delete_stale_records(self):
        Constance = apps.get_model('database.Constance')

        initial_count = Constance.objects.count()

        Constance.objects.create(key='STALE_KEY', value=None)
        call_command('constance', 'remove_stale_keys', stdout=self.out)

        self.assertEqual(Constance.objects.count(), initial_count)
