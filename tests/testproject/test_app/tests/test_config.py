# -*- encoding: utf-8 -*-

import sys
from datetime import datetime, date, time
from decimal import Decimal

from django.test import TestCase
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import IntegrityError

from constance import settings
from constance.admin import Config
from constance.backends.database.models import Constance

# Use django RequestFactory later on
from testproject.test_app.tests.helpers import FakeRequest


class TestStorage(object):

    def test_store(self):
        # read defaults
        del sys.modules['constance']
        from constance import config
        self.assertEquals(config.INT_VALUE, 1)
        self.assertEquals(config.LONG_VALUE, 123456L)
        self.assertEquals(config.BOOL_VALUE, True)
        self.assertEquals(config.STRING_VALUE, 'Hello world')
        self.assertEquals(config.UNICODE_VALUE, u'Rivi\xe8re-Bonjour')
        self.assertEquals(config.DECIMAL_VALUE, Decimal('0.1'))
        self.assertEquals(config.DATETIME_VALUE, datetime(2010, 8, 23, 11, 29, 24))
        self.assertEquals(config.FLOAT_VALUE, 3.1415926536)
        self.assertEquals(config.DATE_VALUE, date(2010, 12, 24))
        self.assertEquals(config.TIME_VALUE, time(23, 59, 59))

        # set values
        config.INT_VALUE = 100
        config.LONG_VALUE = 654321L
        config.BOOL_VALUE = False
        config.STRING_VALUE = 'Beware the weeping angel'
        config.UNICODE_VALUE = 'Québec'.decode('utf-8')
        config.DECIMAL_VALUE = Decimal('1.2')
        config.DATETIME_VALUE = datetime(1977, 10, 2)
        config.FLOAT_VALUE = 2.718281845905
        config.DATE_VALUE = date(2001, 12, 20)
        config.TIME_VALUE = time(1, 59, 0)

        # read again
        self.assertEquals(config.INT_VALUE, 100)
        self.assertEquals(config.LONG_VALUE, 654321L)
        self.assertEquals(config.BOOL_VALUE, False)
        self.assertEquals(config.STRING_VALUE, 'Beware the weeping angel')
        self.assertEquals(config.UNICODE_VALUE, 'Québec'.decode('utf-8'))
        self.assertEquals(config.DECIMAL_VALUE, Decimal('1.2'))
        self.assertEquals(config.DATETIME_VALUE, datetime(1977, 10, 2))
        self.assertEquals(config.FLOAT_VALUE, 2.718281845905)
        self.assertEquals(config.DATE_VALUE, date(2001, 12, 20))
        self.assertEquals(config.TIME_VALUE, time(1, 59, 0))

    def test_nonexistent(self):
        from constance import config
        try:
            config.NON_EXISTENT
        except Exception, e:
            pass
        self.assertEquals(type(e), AttributeError)

        try:
            config.NON_EXISTENT = 1
        except Exception, e:
            pass
        self.assertEquals(type(e), AttributeError)

class TestRedis(TestCase, TestStorage):

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = 'constance.backends.redisd.RedisBackend'
        del sys.modules['constance']
        from constance import config
        config._backend._rd.clear()

    def tearDown(self):
        del sys.modules['constance']
        from constance import config
        config._backend._rd.clear()
        settings.BACKEND = self.old_backend
        import constance
        constance.config = Config()

    def testMissingValues(self):
        from constance import config

        # set some values and leave out others
        config.LONG_VALUE = 654321L
        config.BOOL_VALUE = False
        config.UNICODE_VALUE = 'Québec'.decode('utf-8')
        config.DECIMAL_VALUE = Decimal('1.2')
        config.DATETIME_VALUE = datetime(1977, 10, 2)
        config.DATE_VALUE = date(2001, 12, 20)
        config.TIME_VALUE = time(1, 59, 0)

        self.assertEquals(config.INT_VALUE, 1)  # this should be the default value
        self.assertEquals(config.LONG_VALUE, 654321L)
        self.assertEquals(config.BOOL_VALUE, False)
        self.assertEquals(config.STRING_VALUE, 'Hello world')  # this should be the default value
        self.assertEquals(config.UNICODE_VALUE, 'Québec'.decode('utf-8'))
        self.assertEquals(config.DECIMAL_VALUE, Decimal('1.2'))
        self.assertEquals(config.DATETIME_VALUE, datetime(1977, 10, 2))
        self.assertEquals(config.FLOAT_VALUE, 3.1415926536)  # this should be the default value
        self.assertEquals(config.DATE_VALUE, date(2001, 12, 20))
        self.assertEquals(config.TIME_VALUE, time(1, 59, 0))


class TestDatabase(TestCase, TestStorage):

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = 'constance.backends.database.DatabaseBackend'

    def tearDown(self):
        del sys.modules['constance']
        settings.BACKEND = self.old_backend
        import constance
        constance.config = Config()

    def testUniqueKey(self):
        con = Constance(key='key1', value='value1')
        con.save()
        con2 = Constance(key='key1', value='value2')
        try:
            con2.save()
            self.fail("key field should enforce unique constraint")
        except IntegrityError:
            pass


class TestAdmin(TestCase):
    model = Config

    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'nimda', 'a@a.cz')
        self.options = admin.site._registry[self.model]
        self.fake_request = FakeRequest(user=self.user)
        self.client.login(username=self.user, password='nimda')

    def test_changelist(self):
        response = self.options.changelist_view(self.fake_request, {})
        self.assertEquals(response.status_code, 200)

