Dynamic Django settings in Redis.

Features
========

* Easy migrate your static settings to dynamic settings.
* Admin interface to edit the dynamic settings.

Installation
============

Install from here using ``pip``::

    pip install -e hg+http://bitbucket.org/comoga/django-constance#egg=django-constance

1. Add ``constance`` to your ``INSTALLED_APPS``.

2. Point ``CONSTANCE_CONNECTION`` in your ``settings.py`` to your Redis instance, like this::

        CONSTANCE_CONNECTION = {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
        }

3. Create an empty section ``CONSTANCE_CONFIG`` in your settings which will
   enumerate all your dynamic settings for the admin::

        CONSTANCE_CONFIG = {
        }

Usage
=====

Add

::

    from constance import config

to the top of your source and replace ``settings.MY_SETTINGS_KEY`` with
``config.MY_SETTINGS_KEY`` for each key which you want to be read
from Redis.

Next, move each such key within your ``settings.py`` to the ``CONSTANCE_CONFIG``
section. Keep the default value and add an explanation for the admin, like
this::

    CONSTANCE_CONFIG = {
        'MY_SETTINGS_KEY': (42, 'the answer to everything'),
    }


Fire up your ``admin`` and you should see a new application ``Constance``
with ``MY_SETTINGS_KEY`` in the ``Config`` pseudo model.

