from unittest import mock

from django.test import TestCase

from constance import settings
from constance.checks import check_fieldsets
from constance.checks import get_inconsistent_fieldnames


class ChecksTestCase(TestCase):
    @mock.patch('constance.settings.CONFIG_FIELDSETS', {'Set1': settings.CONFIG.keys()})
    def test_get_inconsistent_fieldnames_none(self):
        """
        Test that get_inconsistent_fieldnames returns an empty data and no checks fail
        if CONFIG_FIELDSETS accounts for every key in settings.CONFIG.
        """
        missing_keys, extra_keys = get_inconsistent_fieldnames()
        self.assertFalse(missing_keys)
        self.assertFalse(extra_keys)

    @mock.patch(
        'constance.settings.CONFIG_FIELDSETS',
        {'Set1': list(settings.CONFIG.keys())[:-1]},
    )
    def test_get_inconsistent_fieldnames_for_missing_keys(self):
        """
        Test that get_inconsistent_fieldnames returns data and the check fails
        if CONFIG_FIELDSETS does not account for every key in settings.CONFIG.
        """
        missing_keys, extra_keys = get_inconsistent_fieldnames()
        self.assertTrue(missing_keys)
        self.assertFalse(extra_keys)
        self.assertEqual(1, len(check_fieldsets()))

    @mock.patch(
        'constance.settings.CONFIG_FIELDSETS',
        {'Set1': [*settings.CONFIG.keys(), 'FORGOTTEN_KEY']},
    )
    def test_get_inconsistent_fieldnames_for_extra_keys(self):
        """
        Test that get_inconsistent_fieldnames returns data and the check fails
        if CONFIG_FIELDSETS contains extra key that is absent in settings.CONFIG.
        """
        missing_keys, extra_keys = get_inconsistent_fieldnames()
        self.assertFalse(missing_keys)
        self.assertTrue(extra_keys)
        self.assertEqual(1, len(check_fieldsets()))

    @mock.patch('constance.settings.CONFIG_FIELDSETS', {})
    def test_check_fieldsets(self):
        """check_fieldsets should not output warning if CONFIG_FIELDSETS is not defined."""
        del settings.CONFIG_FIELDSETS
        self.assertEqual(0, len(check_fieldsets()))
