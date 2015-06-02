Testing
=======

Testing how your app behaves with different config values is achieved with the
:class:`override_config` class. This intentionally mirrors the use of Django's
:class:`~django.test.override_setting`.

.. py:class:: override_config(**kwargs)

    Replace key-value pairs in config.


Usage
~~~~~

It can be used as a decorator at the :class:`~django.test.TestCase` level, the
method level and also as a
`context manager <https://www.python.org/dev/peps/pep-0343/>`_.

.. code-block:: python

    from constance import config
    from constance.test import override_config

    from django.test import TestCase


    @override_config(YOUR_NAME="Arthur of Camelot")
    class ExampleTestCase(TestCase):

        def test_what_is_your_name(self):
            self.assertEqual(config.YOUR_NAME, "Arthur of Camelot")

        @override_config(YOUR_QUEST="To find the Holy Grail")
        def test_what_is_your_quest(self):
            self.assertEqual(config.YOUR_QUEST, "To find the Holy Grail")

        def test_what_is_your_favourite_color(self):
            with override_config(YOUR_FAVOURITE_COLOR="Blue?"):
                self.assertEqual(config.YOUR_FAVOURITE_COLOR, "Blue?")

