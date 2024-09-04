import contextlib
from datetime import datetime
from io import StringIO
from textwrap import dedent

from django.conf import settings
from django.core.management import CommandError
from django.core.management import call_command
from django.test import TransactionTestCase
from django.utils import timezone
from django.utils.encoding import smart_str

from constance import config
from constance.models import Constance


class CliTestCase(TransactionTestCase):
    def setUp(self):
        self.out = StringIO()

    def test_help(self):
        with contextlib.suppress(SystemExit):
            call_command('constance', '--help')

    def test_list(self):
        call_command('constance', 'list', stdout=self.out)

        self.assertEqual(
            set(self.out.getvalue().splitlines()),
            set(
                dedent(
                    smart_str(
                        """        BOOL_VALUE\tTrue
        EMAIL_VALUE\ttest@example.com
        INT_VALUE\t1
        LINEBREAK_VALUE\tSpam spam
        DATE_VALUE\t2010-12-24
        TIME_VALUE\t23:59:59
        TIMEDELTA_VALUE\t1 day, 2:03:00
        STRING_VALUE\tHello world
        CHOICE_VALUE\tyes
        DECIMAL_VALUE\t0.1
        DATETIME_VALUE\t2010-08-23 11:29:24
        FLOAT_VALUE\t3.1415926536
        JSON_VALUE\t{'key': 'value', 'key2': 2, 'key3': [1, 2, 3], 'key4': {'key': 'value'}, 'key5': datetime.date(2019, 1, 1), 'key6': None}
        LIST_VALUE\t[1, '1', datetime.date(2019, 1, 1)]
"""  # noqa: E501
                    )
                ).splitlines()
            ),
        )

    def test_get(self):
        call_command('constance', *('get EMAIL_VALUE'.split()), stdout=self.out)

        self.assertEqual(self.out.getvalue().strip(), 'test@example.com')

    def test_set(self):
        call_command('constance', *('set EMAIL_VALUE blah@example.com'.split()), stdout=self.out)

        self.assertEqual(config.EMAIL_VALUE, 'blah@example.com')

        call_command('constance', *('set', 'DATETIME_VALUE', '2011-09-24', '12:30:25'), stdout=self.out)

        expected = datetime(2011, 9, 24, 12, 30, 25)
        if settings.USE_TZ:
            expected = timezone.make_aware(expected)
        self.assertEqual(config.DATETIME_VALUE, expected)

    def test_get_invalid_name(self):
        self.assertRaisesMessage(
            CommandError,
            'NOT_A_REAL_CONFIG is not defined in settings.CONSTANCE_CONFIG',
            call_command,
            'constance',
            'get',
            'NOT_A_REAL_CONFIG',
        )

    def test_set_invalid_name(self):
        self.assertRaisesMessage(
            CommandError,
            'NOT_A_REAL_CONFIG is not defined in settings.CONSTANCE_CONFIG',
            call_command,
            'constance',
            'set',
            'NOT_A_REAL_CONFIG',
            'foo',
        )

    def test_set_invalid_value(self):
        self.assertRaisesMessage(
            CommandError,
            'Enter a valid email address.',
            call_command,
            'constance',
            'set',
            'EMAIL_VALUE',
            'not a valid email',
        )

    def test_set_invalid_multi_value(self):
        self.assertRaisesMessage(
            CommandError,
            'Enter a list of values.',
            call_command,
            'constance',
            'set',
            'DATETIME_VALUE',
            '2011-09-24 12:30:25',
        )

    def test_delete_stale_records(self):
        initial_count = Constance.objects.count()

        Constance.objects.create(key='STALE_KEY', value=None)
        call_command('constance', 'remove_stale_keys', stdout=self.out)

        self.assertEqual(Constance.objects.count(), initial_count, msg=self.out)
