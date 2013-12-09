# -*- encoding: utf-8 -*-
import six
from datetime import datetime, date, time
from decimal import Decimal

SECRET_KEY = 'cheese'

DATABASE_ENGINE = 'sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'constance',
    'constance.backends.database',
)

ROOT_URLCONF = 'tests.urls'

CONSTANCE_CONNECTION_CLASS = 'tests.redis_mockup.Connection'

long_value = 123456

if not six.PY3:
    long_value = long(long_value)

CONSTANCE_CONFIG = {
    'INT_VALUE': {
        'default': 1,
        'help_text': 'some int',
    },
    'LONG_VALUE': {
        'default': 123456L,
        'help_text': 'some looong int',
    },
    'BOOL_VALUE': {
        'default': True,
        'help_text': 'true or false',
    },
    'STRING_VALUE_REQUIRED': {
        'default': 'Hello world',
        'help_text': 'greetings',
    },
    'STRING_VALUE_NOT_REQUIRED': {
        'default': 'Hello world',
        'help_text': 'greetings',
        'required': False,
    },
    'UNICODE_VALUE': {
        'default': 'Rivière-Bonjour'.decode('utf-8'),
        'help_text': 'greetings',
    },
    'DECIMAL_VALUE': {
        'default': Decimal('0.1'),
        'help_text': 'the first release version',
    },
    'DATETIME_VALUE': {
        'default': datetime(2010, 8, 23, 11, 29, 24),
        'help_text': 'time of the first commit',
    },
    'FLOAT_VALUE': {
        'default': 3.1415926536,
        'help_text': 'PI',
    },
    'DATE_VALUE': {
        'default': date(2010, 12, 24),
        'help_text': 'Merry Chrismas',
    },
    'TIME_VALUE': {
        'default': time(23, 59, 59),
        'help_text': 'And happy New Year',
    },
    'COMPAT_INT_VALUE': (1, 'some int'),
    'COMPAT_LONG_VALUE': (123456L, 'some looong int'),
    'COMPAT_BOOL_VALUE': (True, 'true or false'),
    'COMPAT_STRING_VALUE': ('Hello world', 'greetings'),
    'COMPAT_UNICODE_VALUE': ('Rivière-Bonjour'.decode('utf-8'), 'greetings'),
    'COMPAT_DECIMAL_VALUE': (Decimal('0.1'), 'the first release version'),
    'COMPAT_DATETIME_VALUE': (datetime(2010, 8, 23, 11, 29, 24), 'time of the first commit'),
    'COMPAT_FLOAT_VALUE': (3.1415926536, 'PI'),
    'COMPAT_DATE_VALUE': (date(2010, 12, 24),  'Merry Chrismas'),
    'COMPAT_TIME_VALUE': (time(23, 59, 59),  'And happy New Year'),
}

DEBUG = True

STATIC_ROOT = './static/'

STATIC_URL = '/static/'
