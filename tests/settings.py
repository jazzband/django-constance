# -*- encoding: utf-8 -*-
import django
import six
from datetime import datetime, date, time
from decimal import Decimal


if django.VERSION[:2] < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'

SECRET_KEY = 'cheese'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

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
    'INT_VALUE': (1, 'some int'),
    'LONG_VALUE': (long_value, 'some looong int'),
    'BOOL_VALUE': (True, 'true or false'),
    'STRING_VALUE': ('Hello world', 'greetings'),
    'UNICODE_VALUE': (six.u('Rivière-Bonjour'), 'greetings'),
    'DECIMAL_VALUE': (Decimal('0.1'), 'the first release version'),
    'DATETIME_VALUE': (datetime(2010, 8, 23, 11, 29, 24),
                       'time of the first commit'),
    'FLOAT_VALUE': (3.1415926536, 'PI'),
    'DATE_VALUE': (date(2010, 12, 24), 'Merry Chrismas'),
    'TIME_VALUE': (time(23, 59, 59), 'And happy New Year'),
}

DEBUG = True

STATIC_ROOT = './static/'

STATIC_URL = '/static/'
