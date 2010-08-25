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
}

