.. _backends:

.. highlight:: python

Backends
========

Constance ships with a bunch of backends that are used to store the
configuration values. By default it uses the Redis backend. To override
the default please set the :setting:`CONSTANCE_BACKEND` setting to the appropriate
dotted path.

Configuration values are stored in JSON format and automatically serialized/deserialized
on access.

Redis
-----

The configuration values are stored in a redis store and retrieved using the
`redis-py`_ library. Please install it like this::

  pip install django-constance[redis]

Configuration is simple and defaults to the following value, you don't have
to add it to your project settings::

    CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'

Default redis backend retrieves values every time. There is another redis backend with local cache.
`CachingRedisBackend` stores the value from a redis to memory at first access and checks a value ttl at next.
Configuration installation is simple::

    CONSTANCE_BACKEND = 'constance.backends.redisd.CachingRedisBackend'
    # optionally set a value ttl
    CONSTANCE_REDIS_CACHE_TIMEOUT = 60

.. _`redis-py`: https://pypi.org/project/redis/

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

If you are using `django-redis <https://github.com/jazzband/django-redis>`_,
feel free to use the ``CONSTANCE_REDIS_CONNECTION_CLASS`` setting to define
a callable that returns a redis connection, e.g.::

    CONSTANCE_REDIS_CONNECTION_CLASS = 'django_redis.get_redis_connection'

``CONSTANCE_REDIS_PREFIX``
~~~~~~~~~~~~~~~~~~~~~~~~~~

The (optional) prefix to be used for the key when storing in the Redis
database. Defaults to ``'constance:'``. E.g.::

    CONSTANCE_REDIS_PREFIX = 'constance:myproject:'


``CONSTANCE_REDIS_CACHE_TIMEOUT``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The (optional) ttl of values in seconds used by `CachingRedisBackend` for storing in a local cache.
Defaults to `60` seconds.

Database
--------

Database backend stores configuration values in a standard Django model.

You must set the ``CONSTANCE_BACKEND`` Django setting to::

    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

Please make sure to apply the database migrations::

    python manage.py migrate

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

             If you try this, Constance will throw an error and refuse
             to let your application start. You can work around this by
             subclassing ``constance.backends.database.DatabaseBackend``
             and overriding `__init__` to remove the check. You'll
             want to consult the source code for that function to see
             exactly how.

             We're deliberately being vague about this, because it's
             dangerous; the behavior is undefined, and could even cause
             your app to crash. Nevertheless, there are some limited
             circumstances in which this could be useful, but please
             think carefully before going down this path.

.. note:: By default Constance will autofill the cache on startup and after
          saving any of the config values. If you want to disable the cache
          simply set the :setting:`CONSTANCE_DATABASE_CACHE_AUTOFILL_TIMEOUT`
          setting to ``None``.

Memory
------

The configuration values are stored in a memory and do not persist between process
restarts. In order to use this backend you must set the ``CONSTANCE_BACKEND``
Django setting to::

    CONSTANCE_BACKEND = 'constance.backends.memory.MemoryBackend'

The main purpose of this one is to be used mostly for testing/developing means,
so make sure you intentionally use it on production environments.
