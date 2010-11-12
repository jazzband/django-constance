
"""Borrowed from Carl Meyer's django-adminfiles."""

import os
import sys

parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent)

os.environ['DJANGO_SETTINGS_MODULE'] = 'testproject.settings'

from django.test.simple import run_tests


def runtests():
    failures = run_tests(['test_app'], verbosity=1, interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
