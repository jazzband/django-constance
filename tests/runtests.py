#!/usr/bin/env python
import os
import sys
import django
from django.core.management import call_command

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'


def main():
    if hasattr(django, 'setup'):
        django.setup()
    result = call_command('test', 'tests', verbosity=2)
    sys.exit(result)


if __name__ == '__main__':
    main()
