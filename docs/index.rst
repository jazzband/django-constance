Constance - Dynamic Django settings
===================================

Features
--------

* Easily migrate your static settings to dynamic settings.
* Admin interface to edit the dynamic settings.

.. image:: screenshot2.png

Installation
------------

Install from PyPI the backend specific variant of django-constance:

For the (default) Redis backend::

    pip install "django-constance[redis]"

For the database backend::

    pip install "django-constance[database]"

Alternatively -- if you're sure that the dependencies are already
installed -- you can also run::

    pip install django-constance

Configuration
-------------

Modify your ``settings.py``. Add ``'constance'`` to your
:setting:`INSTALLED_APPS`, and move each key you want to turn dynamic into
the :setting:`CONSTANCE_CONFIG` section, like this:

.. code-block:: python

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.staticfiles',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        ...
        'constance',
    )

    CONSTANCE_CONFIG = {
        'THE_ANSWER': (42, 'Answer to the Ultimate Question of Life, '
                           'The Universe, and Everything'),
    }

Here, ``42`` is the default value for the key ``THE_ANSWER`` if it is
not found in the backend. The other member of the tuple is a help text the
admin will show.

See the :ref:`Backends <backends>` section how to setup the backend and
finish the configuration.

``django-constance``'s hashes generated in different instances of the same
application may differ, preventing data from being saved.

Use this option in order to skip hash verification.

.. code-block:: python

    CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True


Signals
-------

Each time a value is changed it will trigger a ``config_updated`` signal.

You can use it as:

.. code-block:: python

    from constance.signals import config_updated

    @receiver(config_updated)
    def constance_updated(sender, updated_key, new_value, **kwargs):
        print(sender, updated_key, new_value)

The sender is the ``config`` object, and the ``updated_key`` and ``new_value``
are the ones just changed.

This callback will get the ``config`` object as the first parameter so you
can have an isolated function where you can access the ``config`` object
without dealing with additional imports.


Custom fields
-------------

You can set the field type with the third value in the ``CONSTANCE_CONFIG`` tuple.

The value can be one of the supported types or a string matching a key in your :setting:``CONSTANCE_ADDITIONAL_FIELDS``

The supported types are:

* ``bool``
* ``int``
* ``float``
* ``Decimal``
* ``long`` (on python 2)
* ``str``
* ``unicode`` (on python 2)
* ``datetime``
* ``date``
* ``time``

For example, to force a value to be handled as a string:

.. code-block:: python

        'THE_ANSWER': (42, 'Answer to the Ultimate Question of Life, '
                                   'The Universe, and Everything', str),

Custom field types are supported using the dictionary :setting:``CONSTANCE_ADDITIONAL_FIELDS``.

This is a mapping between a field label and a sequence (list or tuple).  The first item in the sequence is the string
path of a field class, and the (optional) second item is a dictionary used to configure the field.

The ``widget`` and ``widget_kwargs`` keys in the field config dictionary can be used to configure the widget used in admin,
the other values will be passed as kwargs to the field's ``__init__()``

Note: Use later evaluated strings instead of direct classes for the field and widget classes:

.. code-block:: python

        CONSTANCE_ADDITIONAL_FIELDS = {
            'yes_no_null_select': ['django.forms.fields.ChoiceField', {
                'widget': 'django.forms.Select',
                'choices': ((None, "-----"), ("yes", "Yes"), ("no", "No"))
            }],
        }

        CONSTANCE_CONFIG = {
            'MY_SELECT_KEY': ('yes', 'select yes or no', 'yes_no_null_select'),
        }

Ordered Fields in Django Admin
------------------------------

In order to Order the fields , you can use OrderedDict collection. Here is an example:

.. code-block:: python

        from collections import OrderedDict

        CONSTANCE_CONFIG = OrderedDict([
            ('SITE_NAME', ('My Title', 'Website title')),
            ('SITE_DESCRIPTION', ('', 'Website description')),
            ('THEME', ('light-blue', 'Website theme')),
        ])


Fieldsets
---------

To group settings together you can define fieldsets. Here's an example:

.. code-block:: python

        CONSTANCE_CONFIG = {
            'SITE_NAME': ('My Title', 'Website title'),
            'SITE_DESCRIPTION': ('', 'Website description'),
            'THEME': ('light-blue', 'Website theme'),
        }

        CONSTANCE_CONFIG_FIELDSETS = {
            'General Options': ('SITE_NAME', 'SITE_DESCRIPTION'),
            'Theme Options': ('THEME',),
        }
.. image:: screenshot3.png

Usage
-----

Constance can be used from your Python code and from your Django templates.

Python
^^^^^^

Accessing the config variables is as easy as importing the config
object and accessing the variables with attribute lookups::

    from constance import config

    # ...

    if config.THE_ANSWER == 42:
        answer_the_question()

Django templates
^^^^^^^^^^^^^^^^

To access the config object from your template you can either
pass the object to the template context:

.. code-block:: python

    from django.shortcuts import render
    from constance import config

    def myview(request):
        return render(request, 'my_template.html', {'config': config})

Or you can use the included config context processor.:

.. code-block:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        # ...
        'constance.context_processors.config',
    )

This will add the config instance to the context of any template
rendered with a ``RequestContext``.

Then, in your template you can refer to the config values just as
any other variable, e.g.:

.. code-block:: django

    <h1>Welcome on {{ config.SITE_NAME }}</h1>
    {% if config.BETA_LAUNCHED %}
        Woohoo! Head over <a href="/sekrit/">here</a> to use the beta.
    {% else %}
        Sadly we haven't launched yet, click <a href="/newsletter/">here</a>
        to signup for our newletter.
    {% endif %}

Command Line
^^^^^^^^^^^^

Constance settings can be get/set on the command line with the manage command `constance`

Available options are:

list - output all values in a tab-separated format::

    $ ./manage.py constance list
    THE_ANSWER 42
    SITE_NAME  My Title

get KEY - output a single values::

    $ ./manage.py constance get THE_ANSWER
    42

set KEY VALUE - set a single value::

    $ ./manage.py constance set SITE_NAME "Another Title"

If the value contains spaces it should be wrapped in quotes.

.. note::  Set values are validated as per in admin, an error will be raised if validation fails:

Eg, given this config as per the example app::

   CONSTANCE_CONFIG = {
       ...
       'DATE_ESTABLISHED': (date(1972, 11, 30), "the shop's first opening"),
   }

Then setting an invalid date will fail as follow::

   $ ./manage.py constance set DATE_ESTABLISHED '1999-12-00'
   CommandError: Enter a valid date.


.. note::  If the admin fields is a `MultiValueField`, (e.g. datetime, which uses `SplitDateTimeField` by default)
then the separate field values need to be provided as separate arguments.

Eg, given this config::

   CONSTANCE_CONFIG = {
       'DATETIME_VALUE': (datetime(2010, 8, 23, 11, 29, 24), 'time of the first commit'),
   }

Then this works (and the quotes are optional)::

   ./manage.py constance set DATETIME_VALUE '2011-09-24' '12:30:25'

This doesn't work::

   ./manage.py constance set DATETIME_VALUE '2011-09-24 12:30:25'
   CommandError: Enter a list of values.

Editing
-------

Fire up your ``admin`` and you should see a new app called ``Constance``
with ``THE_ANSWER`` in the ``Config`` pseudo model.

By default changing the settings via the admin is only allowed for super users.
But in case you want to use the admin's ability to implement custom
authorization checks, feel free to set the :setting:`CONSTANCE_SUPERUSER_ONLY`
setting to ``False`` and give the users or user groups access to the
``constance.change_config`` permission.

.. figure:: screenshot1.png

   The virtual application ``Constance`` among your regular applications.

Custom settings form
--------------------

If you aim at creating a custom settings form this is possible in the following
way: You can inherit from ``ConstanceAdmin`` and set the ``form`` property on
your custom admin to use your custom form. This allows you to define your own
formsets and layouts, similar to defining a custom form on a standard
Django ModelAdmin. This way you can fully style your settings form and group
settings the way you like.

.. code-block:: python

    from constance.admin import ConstanceAdmin, ConstanceForm, Config
    class CustomConfigForm(ConstanceForm):
          def __init__(self, *args, **kwargs):
            super(CustomConfigForm, self).__init__(*args, **kwargs)
            #... do stuff to make your settings form nice ...

    class ConfigAdmin(ConstanceAdmin):
        change_list_form = CustomConfigForm
        change_list_template = 'admin/config/settings.html'

    admin.site.unregister([Config])
    admin.site.register([Config], ConfigAdmin)

You can also override the ``get_changelist_form`` method which is called in
``changelist_view`` to get the actual form used to change the settings. This
allows you to pick a different form according to the user that makes the
request. For example:

.. code-block:: python

    class SuperuserForm(ConstanceForm):
        # Do some stuff here

    class MyConstanceAdmin(ConstanceAdmin):
        def get_changelist_form(self, request):
            if request.user.is_superuser:
              return SuperuserForm:
            else:
              return super(MyConstanceAdmin, self).get_changelist_form(request)

Note that the default method returns ``self.change_list_form``.

More documentation
------------------

.. toctree::
   :maxdepth: 2

   backends
   testing
   changes

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
