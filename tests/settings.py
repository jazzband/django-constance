from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from decimal import Decimal

SECRET_KEY = 'cheese'

MIDDLEWARE = (
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
    },
    'secondary': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
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

CONSTANCE_ADDITIONAL_FIELDS = {
    'yes_no_null_select': [
        'django.forms.fields.ChoiceField',
        {'widget': 'django.forms.Select', 'choices': ((None, '-----'), ('yes', 'Yes'), ('no', 'No'))},
    ],
    # note this intentionally uses a tuple so that we can test immutable
    'email': ('django.forms.fields.EmailField',),
    'array': ['django.forms.fields.CharField', {'widget': 'django.forms.Textarea'}],
    'json': ['django.forms.fields.CharField', {'widget': 'django.forms.Textarea'}],
}

USE_TZ = True

CONSTANCE_CONFIG = {
    'INT_VALUE': (1, 'some int'),
    'BOOL_VALUE': (True, 'true or false'),
    'STRING_VALUE': ('Hello world', 'greetings'),
    'DECIMAL_VALUE': (Decimal('0.1'), 'the first release version'),
    'DATETIME_VALUE': (datetime(2010, 8, 23, 11, 29, 24), 'time of the first commit'),
    'FLOAT_VALUE': (3.1415926536, 'PI'),
    'DATE_VALUE': (date(2010, 12, 24), 'Merry Chrismas'),
    'TIME_VALUE': (time(23, 59, 59), 'And happy New Year'),
    'TIMEDELTA_VALUE': (timedelta(days=1, hours=2, minutes=3), 'Interval'),
    'CHOICE_VALUE': ('yes', 'select yes or no', 'yes_no_null_select'),
    'LINEBREAK_VALUE': ('Spam spam', 'eggs\neggs'),
    'EMAIL_VALUE': ('test@example.com', 'An email', 'email'),
    'LIST_VALUE': ([1, '1', date(2019, 1, 1)], 'A list', 'array'),
    'JSON_VALUE': (
        {
            'key': 'value',
            'key2': 2,
            'key3': [1, 2, 3],
            'key4': {'key': 'value'},
            'key5': date(2019, 1, 1),
            'key6': None,
        },
        'A JSON object',
        'json',
    ),
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
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'constance.context_processors.config',
            ],
        },
    },
]
