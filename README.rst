Constance - Dynamic Django settings
===================================

.. image:: https://secure.travis-ci.org/jezdez/django-constance.png
    :alt: Build Status
    :target: http://travis-ci.org/jezdez/django-constance

A Django app for storing dynamic settings in pluggable backends (Redis and
Django model backend built in) with an integration with the Django admin app.

For more information see the documentation at:

http://django-constance.readthedocs.org/

If you have questions or have trouble using the app please file a bug report
at:

https://github.com/jezdez/django-constance/issues


Changes - add block
===================

original:
'USD_TO_MXN': (16.40, 'Dollar to mexican pesos'),

new version:
'USD_TO_MXN': (16.40, 'Dollar to mexican pesos', 'Finances' ),

if adding third parameter "django constance" grouped the fields in a new block with the name of the third parameter