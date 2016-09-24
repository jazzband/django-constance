# -*- coding: utf-8 -*-

import sys
from contextlib import contextmanager
from textwrap import dedent

from django.core.management import call_command
from django.test import TransactionTestCase
from django.utils import six
from django.utils.six import StringIO


@contextmanager
def redirect_stdout(new_target):
    """
    backport of contextlib.redirect_stdout from http://stackoverflow.com/a/22434262/8331
    :param new_target:
    :return:
    """

    old_target, sys.stdout = sys.stdout, new_target # replace sys.stdout
    try:
        yield new_target # run some code with the replaced stdout
    finally:
        sys.stdout = old_target # restore to the previous value


class CliTestCase(TransactionTestCase):

    def test_help(self):
        out = StringIO()
        try:
            with redirect_stdout(out):
                call_command('constance', '--help')
        except SystemExit:
            pass

    def test_list(self):
        self.maxDiff = None
        out = StringIO()

        with redirect_stdout(out):
            call_command('constance', '--list')

        self.assertEqual(set(out.getvalue().splitlines()), set(dedent(six.u(
"""        BOOL_VALUE	True
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