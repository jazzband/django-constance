#!/usr/bin/env python
import os
import sys
from django.core.management import call_command

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'


def main():
    result = call_command('test', 'tests', verbosity=2)
    sys.exit(result)


if __name__ == '__main__':
    main()
