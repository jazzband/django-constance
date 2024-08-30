Changelog
---------
Starting with version 4.0.0, the changelog is maintained at the GitHub releases `GitHub releases`_

.. _GitHub releases: https://github.com/jazzband/django-constance/releases

v4.0.0 (2024/08/21)
~~~~~~~~~~~~~~~~~~~

* Replace `pickle` with JSON for the database backend
* Fix migration on MySQL
* Fix data loss using `DatabaseBackend` when the DB connection is unstable
* Fix typos in the documentation
* Fix small HTML errors
* Drop support for legacy Django versions
* Migrate JavaScript to ES2015
* Fix documentation build
* Add linters and formatters (using `ruff`)
* Prepare for Django 5.1 support
* Migrate from `setup.py` to `pyproject.toml`
* Bump `tox`
* Declare support for Python 3.12

v3.1.0 (2023/08/21)
~~~~~~~~~~~~~~~~~~~

* Add support for using a subdirectory of `MEDIA_ROOT` for file fields

* Remove pypy from tox tests

v3.0.0 (2023/07/27)
~~~~~~~~~~~~~~~~~~~

* Refactor database backend
  Backward incompatible changes:
  remove ``'constance.backends.database'`` from ``INSTALLED_APPS``

* Dropped support for python < 3.7 and django < 3.2

* Example app now supports django 4.1

* Add support for django 4.2

* Forward the request when saving the admin changelist form

v2.9.1 (2022/08/11)
~~~~~~~~~~~~~~~~~~~

* Add support for gettext in fieldset headers

* Add support for Django 4.1

* Fix text format for MultiValueField usage

v2.9.0 (2022/03/11)
~~~~~~~~~~~~~~~~~~~

* Added arabic translation

* Add concrete_model class attribute to fake admin model

* Added tests for django 3.2

* Fix do not detect datetime fields as date type

* Added support for python 3.10

* Fixes for Ukrainian locale

* Added documentation for constance_dbs config

* Add caching redis backend

* Serialize according to widget

* Add default_auto_field to database backend

v2.8.0 (2020/11/19)
~~~~~~~~~~~~~~~~~~~

* Prevent reset to default for file field

* Fields_list can be a dictionary, when a fieldset is defined as collapsible

* Create and add fa language translations files

* Respect other classes added by admin templates

* Removed deprecated url()

* Use gettext_lazy instead of ugettext_lazy

* Updated python and django version support

v2.7.0 (2020/06/22)
~~~~~~~~~~~~~~~~~~~

* Deleted south migrations

* Improve grammar of documentation index file

* Simplify documentation installation section

* Fix IntegrityError after 2.5.0 release
  (Allow concurrent calls to `DatabaseBackend.set()` method)

* Make groups of fieldsets collapsable

* Allow override_config for pytest

* Put back wheel generation in travis

* Fix wrong "is modified" in admin for multi line strings

* Switch md5 to sha256

* Fix Attempts to change config values fail silently and
  appear to succeed when user does not have change permissions

* Make constance app verbose name translatable

* Update example project for Django>2

* Add anchors in admin for constance settings

* Added a sticky footer in django constance admin

* Add memory backend

* Added Ukrainian locale

* Added lazy checks for pytest

v2.6.0 (2020/01/29)
~~~~~~~~~~~~~~~~~~~

* Drop support py<3.5 django<2.2

* Set pickle protocol version for the Redis backend

* Add a command to delete stale records

v2.5.0 (2019/12/23)
~~~~~~~~~~~~~~~~~~~

* Made results table responsive for Django 2 admin

* Add a Django system check that CONFIG_FIELDSETS accounts for all of CONFIG

* Rewrite set() method of database backend to reduce number of queries

* Fixed "can't compare offset-naive and offset-aware datetimes" when USE_TZ = True

* Fixed compatibility issue with Django 3.0 due to django.utils.six

* Add Turkish language

v2.4.0 (2019/03/16)
~~~~~~~~~~~~~~~~~~~

* Show not existing fields in field_list

* Drop Django<1.11 and 2.0, fix tests vs Django 2.2b

* Fixed "Reset to default" button with constants whose name contains a space

* Use default_storage to save file

* Allow null & blank for PickleField

* Removed Python 3.4 since is not longer supported

v2.3.1 (2018/09/20)
~~~~~~~~~~~~~~~~~~~

* Fixes javascript typo.

v2.3.0 (2018/09/13)
~~~~~~~~~~~~~~~~~~~

* Added zh_Hans translation.

* Fixed TestAdmin.test_linebreaks() due to linebreaksbr() behavior change
  on Django 2.1

* Improved chinese translation

* Fix bug of can't change permission chang_config's name

* Improve consistency of reset value handling for `date`

* Drop support for Python 3.3

* Added official Django 2.0 support.

* Added support for Django 2.1

v2.2.0 (2018/03/23)
~~~~~~~~~~~~~~~~~~~

* Fix ConstanceForm validation.

* `CONSTANCE_DBS` setting for directing constance permissions/content_type
  settings to certain DBs only.

* Added config labels.

* Updated italian translations.

* Fix `CONSTANCE_CONFIG_FIELDSETS` mismatch issue.

v2.1.0 (2018/02/07)
~~~~~~~~~~~~~~~~~~~

* Move inline JavaScript to constance.js.

* Remove translation from the app name.

* Added file uploads.

* Update information on template context processors.

* Allow running set while database is not created.

* Moved inline css/javascripts out to their own files.

* Add French translations.

* Add testing for all supported Python and Django versions.

* Preserve sorting from fieldset config.

* Added datetime.timedelta support.

* Added Estonian translations.

* Account for server timezone for Date object.

v2.0.0 (2017/02/17)
~~~~~~~~~~~~~~~~~~~

* **BACKWARD INCOMPATIBLE** Added the old value to the config_updated signal.

* Added a `get_changelist_form` hook in the ModelAdmin.

* Fix create_perm in apps.py to use database alias given by the post_migrate
  signal.

* Added tests for django 1.11.

* Fix Reset to default to work with boolean/checkboxes.

* Fix handling of MultiValueField's (eg SplitDateTimeField) on the command
  line.

v1.3.4 (2016/12/23)
~~~~~~~~~~~~~~~~~~~

* Fix config ordering issue

* Added localize to check modified flag

* Allow to rename Constance in Admin

* Preserve line breaks in default value

* Added functionality from django-constance-cli

* Added "Reset to default" feature

v1.3.3 (2016/09/17)
~~~~~~~~~~~~~~~~~~~

* Revert broken release

v1.3.2 (2016/09/17)
~~~~~~~~~~~~~~~~~~~

* Fixes a bug where the signal was sent for fields without changes

v1.3.1 (2016/09/15)
~~~~~~~~~~~~~~~~~~~

* Improved the signal path to avoid import errors

* Improved the admin layout when using fieldsets

v1.3 (2016/09/14)
~~~~~~~~~~~~~~~~~

* **BACKWARD INCOMPATIBLE** Dropped support for Django < 1.8).

* Added ordering constance fields using OrderedDict

* Added a signal when updating constance fields

v1.2.1 (2016/09/1)
~~~~~~~~~~~~~~~~~~

* Added some fixes to small bugs

* Fix cache when key changes

* Upgrade django_redis connection string

* Autofill cache key if key is missing

* Added support for fieldsets

v1.2 (2016/05/14)
~~~~~~~~~~~~~~~~~

* Custom Fields were added as a new feature

* Added documentation on how to use Custom settings form

* Introduced ``CONSTANCE_IGNORE_ADMIN_VERSION_CHECK``

* Improved documentation for ``CONSTANCE_ADDITIONAL_FIELDS``

v1.1.2 (2016/02/08)
~~~~~~~~~~~~~~~~~~~

* Moved to Jazzband organization (https://github.com/jazzband/django-constance)

* Added Custom Fields

* Added Django 1.9 support to tests

* Fixes icons for Django 1.9 admin

v1.1.1 (2015/10/01)
~~~~~~~~~~~~~~~~~~~

* Fixed a regression in the 1.1 release that prevented the rendering of the
  admin view with constance values when using the context processor at the
  same time.

v1.1 (2015/09/24)
~~~~~~~~~~~~~~~~~

* **BACKWARD INCOMPATIBLE** Dropped support for Python 2.6
  The supported versions are 2.7, 3.3 (on Django < 1.9) and 3.4.

* **BACKWARD INCOMPATIBLE** Dropped support for Django 1.4, 1.5 and 1.6
  The supported versions are 1.7, 1.8 and the upcoming 1.9 release

* Added compatibility to Django 1.8 and 1.9.

* Added Spanish and Chinese (``zh_CN``) translations.

* Added :class:`override_config` decorator/context manager for easy
  :doc:`testing <testing>`.

* Added the ability to use linebreaks in config value help texts.

* Various testing fixes.

v1.0.1 (2015/01/07)
~~~~~~~~~~~~~~~~~~~

* Fixed issue with import time side effect on Django >= 1.7.

v1.0 (2014/12/04)
~~~~~~~~~~~~~~~~~

* Added docs and set up Read The Docs project:

  https://django-constance.readthedocs.io/

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
