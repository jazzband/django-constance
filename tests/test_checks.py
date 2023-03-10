import datetime
from decimal import Decimal
from unittest import mock

from constance.admin import get_values
from constance.checks import check_fieldsets, get_inconsistent_fieldnames
from constance.management.commands.constance import _set_constance_value
from django.core.exceptions import ValidationError
from django.test import TestCase
from constance import settings


class ChecksTestCase(TestCase):
    @mock.patch("constance.settings.CONFIG_FIELDSETS", {"Set1": settings.CONFIG.keys()})
    def test_get_inconsistent_fieldnames_none(self):
        """
        Test that get_inconsistent_fieldnames returns an empty set and no checks fail
        if CONFIG_FIELDSETS accounts for every key in settings.CONFIG.
        """
        self.assertFalse(get_inconsistent_fieldnames())
        self.assertEqual(0, len(check_fieldsets()))

    @mock.patch(
        "constance.settings.CONFIG_FIELDSETS",
        {"Set1": list(settings.CONFIG.keys())[:-1]},
    )
    def test_get_inconsistent_fieldnames_one(self):
        """
        Test that get_inconsistent_fieldnames returns a set and the check fails
        if CONFIG_FIELDSETS does not account for every key in settings.CONFIG.
        """
        self.assertTrue(get_inconsistent_fieldnames())
        self.assertEqual(1, len(check_fieldsets()))

    @mock.patch(
        "constance.settings.CONFIG_FIELDSETS", {}
    )
    def test_check_fieldsets(self):
        """
        check_fieldsets should not output warning if CONFIG_FIELDSETS is not defined.
        """
        del settings.CONFIG_FIELDSETS
        self.assertEqual(0, len(check_fieldsets()))
