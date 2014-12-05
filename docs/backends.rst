.. _backends:

.. highlight:: python

Backends
========

Constance ships with a bunch of backends that are used to store the
configuration values. By default it uses the Redis backend. To override
the default please set the :setting:`CONSTANCE_BACKEND` setting to the appropriate
dotted path.

Redis
-----

The configuration values are stored in a redis store and retrieved using the
`redis-py`_ library. Please install it like this::

  pip install django-constance[redis]

Configuration is simple and defaults to the following value, you don't have
to add it to your project settings::

    CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'

.. _`redis-py`: https://pypi.python.org/pypi/redis

Settings
^^^^^^^^

There are a couple of options:

``CONSTANCE_REDIS_CONNECTION``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A dictionary of parameters to pass to the to Redis client, e.g.::

    CONSTANCE_REDIS_CONNECTION = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
    }

Alternatively you can use a URL to do the same::

    CONSTANCE_REDIS_CONNECTION = 'redis://username:password@localhost:6379/0'

``CONSTANCE_REDIS_CONNECTION_CLASS``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An (optional) dotted import path to a connection to use, e.g.::

    CONSTANCE_REDIS_CONNECTION_CLASS = 'myproject.myapp.mockup.Connection'

If you are using `django-redis <http://niwibe.github.io/django-redis/>`_,
feel free to use the ``CONSTANCE_REDIS_CONNECTION_CLASS`` setting to define
a callable that returns a redis connection, e.g.::

    CONSTANCE_REDIS_CONNECTION_CLASS = 'redis_cache.get_redis_connection'

``CONSTANCE_REDIS_PREFIX``
~~~~~~~~~~~~~~~~~~~~~~~~~~

The (optional) prefix to be used for the key when storing in the Redis
database. Defaults to ``'constance:'``. E.g.::

    CONSTANCE_REDIS_PREFIX = 'constance:myproject:'

Database
--------

The database backend is optional and stores the configuration values in a
standard Django model. It requires the package `django-picklefield`_ for
storing those values. Please install it like so::

  pip install django-constance[database]

You must set the ``CONSTANCE_BACKEND`` Django setting to::

    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

Then add the database backend app to your :setting:`INSTALLED_APPS` setting to
make sure the data model is correctly created::

    INSTALLED_APPS = (
        # other apps
        'constance.backends.database',
    )

Please make sure to apply the database migrations::

    python manage.py migrate database

.. note:: If you're upgrading Constance to 1.0 and use Django 1.7 or higher
          please make sure to let the migration system know that you've
          already created the tables for the database backend.

          You can do that using the ``--fake`` option of the migrate command::

              python manage.py migrate database --fake

Just like the Redis backend you can set an optional prefix that is used during
database interactions (it defaults to an empty string, ``''``). To use
something else do this::

    CONSTANCE_DATABASE_PREFIX = 'constance:myproject:'

Caching
^^^^^^^

The database backend has the ability to automatically cache the config
values and clear them when saving. Assuming you have a :setting:`CACHES`
setting set you only need to set the the
:setting:`CONSTANCE_DATABASE_CACHE_BACKEND` setting to the name of the
configured cache backend to enable this feature, e.g. "default"::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
    CONSTANCE_DATABASE_CACHE_BACKEND = 'default'

.. warning:: The cache feature won't work with a cache backend that is
             incompatible with cross-process caching like the local memory
             cache backend included in Django because correct cache
             invalidation can't be guaranteed.

.. note:: By default Constance will autofill the cache on startup and after
          saving any of the config values. If you want to disable the cache
          simply set the :setting:`CONSTANCE_DATABASE_CACHE_AUTOFILL_TIMEOUT`
          setting to ``None``.

.. _django-picklefield: http://pypi.python.org/pypi/django-picklefield/
