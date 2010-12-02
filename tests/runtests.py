#!/usr/bin/env python

"""Borrowed from Carl Meyer's django-adminfiles."""

import os
import sys

currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, currentdir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'testproject.settings'

from django.test.simple import run_tests


def main():
    failures = run_tests(['test_app'], verbosity=1, interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    main()
