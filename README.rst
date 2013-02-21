Dynamic Django settings
=======================

Features
--------

* Easily migrate your static settings to dynamic settings.
* Admin interface to edit the dynamic settings.

Installation
------------

Install from PyPI::

    pip install django-constance

Or install the `in-development version`_ using ``pip``::

    pip install -e git+git://github.com/comoga/django-constance#egg=django-constance

.. _`in-development version`: https://github.com/comoga/django-constance/tarball/master#egg=django-constance-dev

Configuration
-------------

Modify your ``settings.py``. Add ``'constance'`` to your ``INSTALLED_APPS``,
and move each key you want to turn dynamic into the ``CONSTANCE_CONFIG``
section, like this::

    INSTALLED_APPS = (
        ...
        'constance',
    )

    CONSTANCE_CONFIG = {
        'MY_SETTINGS_KEY': (42, 'the answer to everything'),
    }

Here, ``42`` is the default value for the key ``MY_SETTINGS_KEY`` if it is
not found in the backend. The other member of the tuple is a help text the
admin will show.

See the `Backends`_ section how to setup the backend.

Backends
~~~~~~~~

Constance ships with a bunch of backends that are used to store the
configuration values. By default it uses the Redis backend. To override
the default please set the ``CONSTANCE_BACKEND`` setting to the appropriate
dotted path.

Redis (default)
+++++++++++++++

::

    CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'

The is the default backend and has a couple of options:

* ``CONSTANCE_REDIS_CONNECTION``

  A dictionary of parameters to pass to the to Redis client, e.g.::

    CONSTANCE_REDIS_CONNECTION = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
    }

  Alternatively you can use a URL to do the same::

    CONSTANCE_REDIS_CONNECTION = 'redis://username:password@localhost:6379/0'

* ``CONSTANCE_REDIS_CONNECTION_CLASS``

  An (optional) dotted import path to a connection to use, e.g.::

    CONSTANCE_REDIS_CONNECTION_CLASS = 'myproject.myapp.mockup.Connection'

* ``CONSTANCE_REDIS_PREFIX``

  The (optional) prefix to be used for the key when storing in the Redis
  database. Defaults to ``'constance:'``. E.g.::

    CONSTANCE_REDIS_PREFIX = 'constance:myproject:'

Database
++++++++

::

    CONSTANCE_BACKEND = constance.backends.database.DatabaseBackend

If you want to use this backend you also need to add the databse backend
to your ``INSTALLED_APPS`` setting to make sure the data model is correctly
created::

    INSTALLED_APPS = (
        # other apps
        'constance.backends.database',
    )

It also uses `django-picklefield`_ to store the values in the database, so
you need to install this library, too. E.g.::

    pip install django-picklefield

The database backend has the ability to automatically cache the config
values and clear them when saving. You need to set the following setting
to enable this feature::

    CONSTANCE_DATABASE_CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

.. note:: This won't work with a cache backend that doesn't support
   cross-process caching, because correct cache invalidation
   can't be guaranteed.

Starting in Django 1.3 you can alternatively be the name of an entry of
the ``CACHES`` setting. E.g.::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
    CONSTANCE_DATABASE_CACHE_BACKEND = 'default'

.. _django-picklefield: http://pypi.python.org/pypi/django-picklefield/

Usage
-----

Constance can be used from your Python code and from your Django templates.

* Python

  Accessing the config variables is as easy as importing the config
  object and accessing the variables with attribute lookups::

    from constance import config

    # ...

    if config.MY_SETTINGS_KEY == 42:
        answer_the_question()

* Django templates

  To access the config object from your template, you can either
  pass the object to the template context::

    from django.shortcuts import render_to_response
    from constance import config

    def myview(request):
        return render_to_response('my_template.html', {'config': config})

  Or you can use the included config context processor.::

    TEMPLATE_CONTEXT_PROCESSORS = (
        # ...
        'constance.context_processors.config',
    )

  This will add the config instance to the context of any template
  rendered with a ``RequestContext``.

  Then, in your template you can refer to the config values just as
  any other variable, e.g.::

    <h1>Welcome on {% config.SITE_NAME %}</h1>
    {% if config.BETA_LAUNCHED %}
        Woohoo! Head over <a href="/sekrit/">here</a> to use the beta.
    {% else %}
        Sadly we haven't launched yet, click <a href="/newsletter/">here</a>
        to signup for our newletter.
    {% endif %}

Editing
~~~~~~~

Fire up your ``admin`` and you should see a new app called ``Constance``
with ``MY_SETTINGS_KEY`` in the ``Config`` pseudo model.

By default changing the settings via the admin is only allowed for super users.
But in case you want to use the admin's ability to implement custom
authorization checks, feel free to set the ``CONSTANCE_SUPERUSER_ONLY`` setting
to ``False`` and give the users or user groups access to the
``constance.change_config`` permission.

Screenshots
-----------

.. figure:: https://github.com/comoga/django-constance/raw/master/docs/screenshot2.png

   The standard edit screen.

.. figure:: https://github.com/comoga/django-constance/raw/master/docs/screenshot1.png

   The virtual application ``Constance`` among your regular applications.


