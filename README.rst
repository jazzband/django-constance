Dynamic Django settings in Redis.

Features
========

* Easy migrate your static settings to dynamic settings.
* Admin interface to edit the dynamic settings.

Installation
============

Install from here using ``pip``::

    pip install -e hg+http://bitbucket.org/comoga/django-constance#egg=django-constance

Configuration
=============

Modify your ``settings.py``. Add ``constance`` to your ``INSTALLED_APPS``,
point ``CONSTANCE_CONNECTION`` to your Redis instance, and move each
key you want to turn dynamic into the ``CONSTANCE_CONFIG`` section, like this::


    INSTALLED_APPS = (
        ...
        'constance',
    )

    CONSTANCE_CONNECTION = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
    }


    CONSTANCE_CONFIG = {
        'MY_SETTINGS_KEY': (42, 'the answer to everything'),
    }

Here, ``42`` is the default value for the key MY_SETTINGS_KEY if it is not
found in Redis. The other member of the tuple is a help text the admin
will show.

Usage
=====

::

    from constance import config

    ...

    if config.MY_SETTINGS_KEY == 42:
        answer_the_question()


Fire up your ``admin`` and you should see a new application ``Constance``
with ``MY_SETTINGS_KEY`` in the ``Config`` pseudo model.

Screenshots
===========

.. figure:: http://bitbucket.org/comoga/django-constance/wiki/screenshot2.png

   The standard edit screen.

.. figure:: http://bitbucket.org/comoga/django-constance/wiki/screenshot1.png

   The virtual application ``Constance`` among your regular applications.


