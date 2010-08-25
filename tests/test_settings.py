DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}


CONSTANCE_CONNECTION_CLASS = 'tests.redis_mockup.Connection'

INSTALLED_APPS = (
    'tests',
    'constance',
)

