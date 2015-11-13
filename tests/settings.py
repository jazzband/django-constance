# -*- encoding: utf-8 -*-
import django
from django.utils import six

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

CONSTANCE_REDIS_CONNECTION_CLASS = 'tests.redis_mockup.Connection'

long_value = 123456

if not six.PY3:
    long_value = long(long_value)

CONSTANCE_ADDITIONAL_FIELDS = {
     'yes_no_null_select': ['django.forms.fields.ChoiceField',
         {
         'widget': 'django.forms.Select',
         'choices': (("-----", None), ("yes", "Yes"), ("no", "No"))
         }],
     }

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
    'CHOICE_VALUE': ('yes', 'select yes or no', 'yes_no_null_select'),
    'LINEBREAK_VALUE': ('Spam spam', 'eggs\neggs'),
}

DEBUG = True

STATIC_ROOT = './static/'

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'constance.context_processors.config',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'constance.context_processors.config',
)
