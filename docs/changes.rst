Changelog
---------

v1.0.1 (2015/01/07)
~~~~~~~~~~~~~~~~~~~

* Fixed issue with import time side effect on Django >= 1.7.

v1.0 (2014/12/04)
~~~~~~~~~~~~~~~~~

* Added docs and set up Read The Docs project:

  http://django-constance.readthedocs.org/

* Set up Transifex project for easier translations:

  https://www.transifex.com/projects/p/django-constance

* Added autofill feature for the database backend cache which is enabled
  by default.

* Added Django>=1.7 migrations and moved South migrations to own folder.
  Please upgrade to South>=1.0 to use the new South migration location.

  For Django 1.7 users that means running the following to fake the migration::

    django-admin.py migrate database --fake

* Added consistency check when saving config values in the admin to prevent
  accidentally overwriting other users' changes.

* Fixed issue with South migration that would break on MySQL.

* Fix compatibility with Django 1.6 and 1.7 and current master (to be 1.8).

* Fixed clearing database cache en masse by applying prefix correctly.

* Fixed a few translation related issues.

* Switched to tox as test script.

* Fixed a few minor cosmetic frontend issues
  (e.g. padding in admin table header).

* Deprecated a few old settings:

  ============================== ===================================
  deprecated                     replacement
  ============================== ===================================
  ``CONSTANCE_CONNECTION_CLASS`` ``CONSTANCE_REDIS_CONNECTION_CLASS``
  ``CONSTANCE_CONNECTION``       ``CONSTANCE_REDIS_CONNECTION``
  ``CONSTANCE_PREFIX``           ``CONSTANCE_REDIS_PREFIX``
  ============================== ===================================

* The undocumented feature to use an environment variable called
  ``CONSTANCE_SETTINGS_MODULE`` to define which module to load
  settings from has been removed.

v0.6 (2013/04/12)
~~~~~~~~~~~~~~~~~

* Added Python 3 support. Supported versions: 2.6, 2.7, 3.2 and 3.3.
  For Python 3.x the use of Django > 1.5.x is required.

* Fixed a serious issue with ordering in the admin when using the database
  backend. Thanks, Bouke Haarsma.

* Switch to django-discover-runner as test runner to be able to run on
  Python 3.

* Fixed an issue with refering to static files in the admin interface
  when using Django < 1.4.

v0.5 (2013/03/02)
~~~~~~~~~~~~~~~~~

* Fixed compatibility with Django 1.5's swappable model backends.

* Converted the ``key`` field of the database backend to use a ``CharField``
  with uniqueness instead of just ``TextField``.

  For South users we provide a migration for that change. First you
  have to "fake" the initial migration we've also added to this release::

    django-admin.py migrate database --fake 0001

  After that you can run the rest of the migrations::

    django-admin.py migrate database

* Fixed compatibility with Django>1.4's way of refering to static files in
  the admin.

* Added ability to add custom authorization checks via the new
  ``CONSTANCE_SUPERUSER_ONLY`` setting.

* Added Polish translation. Thanks, Janusz Harkot.

* Allow ``CONSTANCE_REDIS_CONNECTION`` being an URL instead of a dict.

* Added ``CONSTANCE_DATABASE_PREFIX`` setting allow setting a key prefix.

* Switched test runner to use django-nose.
