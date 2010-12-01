# -*- encoding: utf-8 -*-

from datetime import datetime, date, time
from decimal import Decimal

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.admin',

    'constance',
    'constance.backends.database',

    'testproject.test_app',
)

ROOT_URLCONF = 'testproject.urls'

CONSTANCE_CONNECTION_CLASS = 'testproject.test_app.redis_mockup.Connection'

CONSTANCE_CONFIG = {
    'INT_VALUE': (1, 'some int'),
    'LONG_VALUE': (123456L, 'some looong int'),
    'BOOL_VALUE': (True, 'true or false'),
    'STRING_VALUE': ('Hello world', 'greetings'),
    'UNICODE_VALUE': ('Rivière-Bonjour'.decode('utf-8'), 'greetings'),
    'DECIMAL_VALUE': (Decimal('0.1'), 'the first release version'),
    'DATETIME_VALUE': (datetime(2010, 8, 23, 11, 29, 24), 'time of the first commit'),
    'FLOAT_VALUE': (3.1415926536, 'PI'),
    'DATE_VALUE': (date(2010, 12, 24),  'Merry Chrismas'),
    'TIME_VALUE': (time(23, 59, 59),  'And happy New Year'),
}
