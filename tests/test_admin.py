from datetime import datetime
from unittest import mock

from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.template.defaultfilters import linebreaksbr
from django.test import RequestFactory
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from constance import settings
from constance.admin import Config
from constance.forms import ConstanceForm
from constance.utils import get_values


class TestAdmin(TestCase):
    model = Config

    def setUp(self):
        super().setUp()
        self.rf = RequestFactory()
        self.superuser = User.objects.create_superuser('admin', 'nimda', 'a@a.cz')
        self.normaluser = User.objects.create_user('normal', 'nimda', 'b@b.cz')
        self.normaluser.is_staff = True
        self.normaluser.save()
        self.options = admin.site._registry[self.model]

    def test_changelist(self):
        self.client.login(username='admin', password='nimda')
        request = self.rf.get('/admin/constance/config/')
        request.user = self.superuser
        response = self.options.changelist_view(request, {})
        self.assertEqual(response.status_code, 200)

    def test_custom_auth(self):
        settings.SUPERUSER_ONLY = False
        self.client.login(username='normal', password='nimda')
        request = self.rf.get('/admin/constance/config/')
        request.user = self.normaluser
        self.assertRaises(PermissionDenied, self.options.changelist_view, request, {})
        self.assertFalse(request.user.has_perm('constance.change_config'))

        # reload user to reset permission cache
        request = self.rf.get('/admin/constance/config/')
        request.user = User.objects.get(pk=self.normaluser.pk)

        request.user.user_permissions.add(Permission.objects.get(codename='change_config'))
        self.assertTrue(request.user.has_perm('constance.change_config'))

        response = self.options.changelist_view(request, {})
        self.assertEqual(response.status_code, 200)

    def test_linebreaks(self):
        self.client.login(username='admin', password='nimda')
        request = self.rf.get('/admin/constance/config/')
        request.user = self.superuser
        response = self.options.changelist_view(request, {})
        self.assertContains(response, 'LINEBREAK_VALUE')
        self.assertContains(response, linebreaksbr('eggs\neggs'))

    @mock.patch(
        'constance.settings.CONFIG_FIELDSETS',
        {
            'Numbers': ('INT_VALUE',),
            'Text': ('STRING_VALUE',),
        },
    )
    def test_fieldset_headers(self):
        self.client.login(username='admin', password='nimda')
        request = self.rf.get('/admin/constance/config/')
        request.user = self.superuser
        response = self.options.changelist_view(request, {})
        self.assertContains(response, '<h2>Numbers</h2>')
        self.assertContains(response, '<h2>Text</h2>')

    @mock.patch(
        'constance.settings.CONFIG_FIELDSETS',
        (
            ('Numbers', ('INT_VALUE',)),
            ('Text', ('STRING_VALUE',)),
        ),
    )
    def test_fieldset_tuple(self):
        self.client.login(username='admin', password='nimda')
        request = self.rf.get('/admin/constance/config/')
        request.user = self.superuser
        response = self.options.changelist_view(request, {})
        self.assertContains(response, '<h2>Numbers</h2>')
        self.assertContains(response, '<h2>Text</h2>')

    @mock.patch(
        'constance.settings.CONFIG_FIELDSETS',
        {
            'Numbers': {
                'fields': (
                    'INT_VALUE',
                    'DECIMAL_VALUE',
                ),
                'collapse': True,
            },
            'Text': {
                'fields': (
                    'STRING_VALUE',
                    'LINEBREAK_VALUE',
                ),
                'collapse': True,
            },
        },
    )
    def test_collapsed_fieldsets(self):
        self.client.login(username='admin', password='nimda')
        request = self.rf.get('/admin/constance/config/')
        request.user = self.superuser
        response = self.options.changelist_view(request, {})
        self.assertContains(response, 'module collapse')

    @mock.patch('constance.settings.CONFIG_FIELDSETS', {'FieldSetOne': ('INT_VALUE',)})
    @mock.patch(
        'constance.settings.CONFIG',
        {
            'INT_VALUE': (1, 'some int'),
        },
    )
    @mock.patch('constance.settings.IGNORE_ADMIN_VERSION_CHECK', True)
    @mock.patch('constance.forms.ConstanceForm.save', lambda _: None)
    @mock.patch('constance.forms.ConstanceForm.is_valid', lambda _: True)
    def test_submit(self):
        """
        Test that submitting the admin page results in an http redirect when
        everything is in order.
        """
        initial_value = {'INT_VALUE': settings.CONFIG['INT_VALUE'][0]}

        self.client.login(username='admin', password='nimda')

        request = self.rf.post(
            '/admin/constance/config/',
            data={
                **initial_value,
                'version': '123',
            },
        )

        request.user = self.superuser
        request._dont_enforce_csrf_checks = True

        with mock.patch('django.contrib.messages.add_message') as mock_message, mock.patch.object(
            ConstanceForm, '__init__', **initial_value, return_value=None
        ) as mock_form:
            response = self.options.changelist_view(request, {})
            mock_form.assert_called_with(data=request.POST, files=request.FILES, initial=initial_value, request=request)
            mock_message.assert_called_with(request, 25, _('Live settings updated successfully.'))

        self.assertIsInstance(response, HttpResponseRedirect)

    @mock.patch('constance.settings.CONFIG_FIELDSETS', {'FieldSetOne': ('MULTILINE',)})
    @mock.patch(
        'constance.settings.CONFIG',
        {
            'MULTILINE': ('Hello\nWorld', 'multiline value'),
        },
    )
    @mock.patch('constance.settings.IGNORE_ADMIN_VERSION_CHECK', True)
    def test_newlines_normalization(self):
        self.client.login(username='admin', password='nimda')
        request = self.rf.post(
            '/admin/constance/config/',
            data={
                'MULTILINE': 'Hello\r\nWorld',
                'version': '123',
            },
        )
        request.user = self.superuser
        request._dont_enforce_csrf_checks = True
        with mock.patch('django.contrib.messages.add_message'):
            response = self.options.changelist_view(request, {})
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(get_values()['MULTILINE'], 'Hello\nWorld')

    @mock.patch(
        'constance.settings.CONFIG',
        {
            'DATETIME_VALUE': (datetime(2019, 8, 7, 18, 40, 0), 'some naive datetime'),
        },
    )
    @mock.patch('constance.settings.IGNORE_ADMIN_VERSION_CHECK', True)
    @mock.patch('tests.redis_mockup.Connection.set', mock.MagicMock())
    def test_submit_aware_datetime(self):
        """
        Test that submitting the admin page results in an http redirect when
        everything is in order.
        """
        request = self.rf.post(
            '/admin/constance/config/',
            data={
                'DATETIME_VALUE_0': '2019-08-07',
                'DATETIME_VALUE_1': '19:17:01',
                'version': '123',
            },
        )
        request.user = self.superuser
        request._dont_enforce_csrf_checks = True
        with mock.patch('django.contrib.messages.add_message'):
            response = self.options.changelist_view(request, {})
        self.assertIsInstance(response, HttpResponseRedirect)

    @mock.patch(
        'constance.settings.CONFIG_FIELDSETS',
        {
            'Numbers': ('INT_VALUE',),
            'Text': ('STRING_VALUE',),
        },
    )
    def test_inconsistent_fieldset_submit(self):
        """
        Test that the admin page warns users if the CONFIG_FIELDSETS setting
        doesn't account for every field in CONFIG.
        """
        self.client.login(username='admin', password='nimda')
        request = self.rf.post('/admin/constance/config/', data=None)
        request.user = self.superuser
        request._dont_enforce_csrf_checks = True
        with mock.patch('django.contrib.messages.add_message'):
            response = self.options.changelist_view(request, {})
        self.assertContains(response, 'is missing field(s)')

    @mock.patch(
        'constance.settings.CONFIG_FIELDSETS',
        {
            'Fieldsets': (
                'STRING_VALUE',
                'INT_VALUE',
            ),
        },
    )
    def test_fieldset_ordering_1(self):
        """Ordering of inner list should be preserved."""
        self.client.login(username='admin', password='nimda')
        request = self.rf.get('/admin/constance/config/')
        request.user = self.superuser
        response = self.options.changelist_view(request, {})
        response.render()
        content_str = response.content.decode()
        self.assertGreater(content_str.find('INT_VALUE'), content_str.find('STRING_VALUE'))

    @mock.patch(
        'constance.settings.CONFIG_FIELDSETS',
        {
            'Fieldsets': (
                'INT_VALUE',
                'STRING_VALUE',
            ),
        },
    )
    def test_fieldset_ordering_2(self):
        """Ordering of inner list should be preserved."""
        self.client.login(username='admin', password='nimda')
        request = self.rf.get('/admin/constance/config/')
        request.user = self.superuser
        response = self.options.changelist_view(request, {})
        response.render()
        content_str = response.content.decode()
        self.assertGreater(content_str.find('STRING_VALUE'), content_str.find('INT_VALUE'))

    def test_labels(self):
        self.assertEqual(type(self.model._meta.label), str)
        self.assertEqual(type(self.model._meta.label_lower), str)
