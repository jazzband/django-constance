from datetime import datetime
from decimal import Decimal

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'tests',
    'constance',
)

CONSTANCE_CONNECTION_CLASS = 'tests.redis_mockup.Connection'

CONSTANCE_CONFIG = {
    'INT_VALUE': (1, 'some int'),
    'BOOL_VALUE': (True, 'true or false'),
    'STRING_VALUE': ('Hello world', 'greetings'),
    'DECIMAL_VALUE': (Decimal('0.1'), 'the first release version'),
    'DATETIME_VALUE': (datetime(2010, 8, 23, 11, 29, 24), 'time of the first commit'),
    'FLOAT_VALUE': (3.1415926536, 'PI'),
}
