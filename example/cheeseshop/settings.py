"""
Django settings for cheeseshop project.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SITE_ID = 1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hdx64#m+lnc_0ffoyehbk&7gk1&*9uar$pcfcm-%$km#p0$k=6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cheeseshop.apps.catalog',
    'cheeseshop.apps.storage',
    'constance',
)

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'cheeseshop.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'cheeseshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/cheeseshop.db',
    }
}

CONSTANCE_REDIS_CONNECTION = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

CONSTANCE_ADDITIONAL_FIELDS = {
    'yes_no_null_select': [
        'django.forms.fields.ChoiceField',
        {'widget': 'django.forms.Select', 'choices': ((None, '-----'), ('yes', 'Yes'), ('no', 'No'))},
    ],
    'email': ('django.forms.fields.EmailField',),
    'json_field': ['cheeseshop.fields.JsonField'],
    'image_field': ['django.forms.ImageField', {}],
}

CONSTANCE_CONFIG = {
    'BANNER': ('The National Cheese Emporium', 'name of the shop'),
    'OWNER': ('Mr. Henry Wensleydale', 'owner of the shop'),
    'OWNER_EMAIL': ('henry@example.com', 'contact email for owner', 'email'),
    'MUSICIANS': (4, 'number of musicians inside the shop'),
    'DATE_ESTABLISHED': (date(1972, 11, 30), "the shop's first opening"),
    'MY_SELECT_KEY': ('yes', 'select yes or no', 'yes_no_null_select'),
    'MULTILINE': ('Line one\nLine two', 'multiline string'),
    'JSON_DATA': (
        {'a': 1_000, 'b': 'test', 'max': 30_000_000},
        'Some test data for json',
        'json_field',
    ),
    'LOGO': (
        '',
        'Logo image file',
        'image_field',
    ),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'Cheese shop general info': [
        'BANNER',
        'OWNER',
        'OWNER_EMAIL',
        'MUSICIANS',
        'DATE_ESTABLISHED',
        'LOGO',
    ],
    'Awkward test settings': ['MY_SELECT_KEY', 'MULTILINE', 'JSON_DATA'],
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
CONSTANCE_DATABASE_CACHE_BACKEND = 'default'

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CONSTANCE_FILE_ROOT = 'constance'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
