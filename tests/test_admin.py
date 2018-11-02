# set encoding=utf8
import mock
from django.contrib import admin
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.template.defaultfilters import linebreaksbr
from django.test import TestCase, RequestFactory
from django.utils import six
from django.views.decorators.csrf import csrf_exempt
from constance import settings
from constance.admin import Config
from django.utils.decorators import method_decorator
from django.contrib.messages.storage.fallback import FallbackStorage
import datetime
from decimal import Decimal

class TestAdmin(TestCase):
    model = Config

    def setUp(self):
        super(TestAdmin, self).setUp()
        self.rf = RequestFactory()
        self.superuser = User.objects.create_superuser('admin', 'nimda', 'a@a.cz')
        self.normaluser = User.objects.create_user('normal', 'nimda', 'b@b.cz')
        self.normaluser.is_staff = True
        self.normaluser.save()
        self.options = admin.site._registry[self.model]

    @mock.patch("constance.admin.ConstanceForm.clean_version", lambda x: 'test')
    def test_changelist_post(self):
        self.client.login(username='admin', password='nimda')
        data = {
            'FLOAT_VALUE': 3.1415926536,
            'BOOL_VALUE': True,
            'EMAIL_VALUE': 'test@example.com',
            'INT_VALUE': 1,
            'CHOICE_VALUE': 'yes',
            'TIME_VALUE': datetime.time(23, 59, 59),
            'DATE_VALUE': datetime.date(2010, 12, 24),
            'TIMEDELTA_VALUE': datetime.timedelta(days=1, hours=2, minutes=3),
            'LINEBREAK_VALUE': 'Spam spam',
            'DECIMAL_VALUE': Decimal('0.1'),
            'STRING_VALUE': 'Hello world',
            'UNICODE_VALUE': u'Rivière-Bonjour რუსთაველი',
            'DATETIME_VALUE': datetime.datetime(2010, 8, 23, 11, 29, 24),
            'LONG_VALUE': 123456,
            'DATETIME_VALUE_0': datetime.datetime(2010, 8, 23, 11, 29, 24).strftime("%Y-%m-%d"),
            'DATETIME_VALUE_1': datetime.datetime(2010, 8, 23, 11, 29, 24).strftime("%H:%M:%S"),
            'version': 'test'
        }
        request = self.rf.post('/admin/constance/config/', data, follow=True)
        request._dont_enforce_csrf_checks=True
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.superuser
        response = self.options.changelist_view(request, {})
        self.assertEqual(response.status_code, 302)

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
        self.assertRaises(PermissionDenied,
                          self.options.changelist_view,
                          request, {})
        self.assertFalse(request.user.has_perm('constance.change_config'))

        # reload user to reset permission cache
        request = self.rf.get('/admin/constance/config/')
        request.user = User.objects.get(pk=self.normaluser.pk)

        request.user.user_permissions.add(Permission.objects.get(codename='change_config'))
        self.assertTrue(request.user.has_perm('constance.change_config'))

        response = self.options.changelist_view(request, {})
        self.assertEqual(response.status_code, 200)

    def test_str(self):
        ct = ContentType.objects.get(app_label='constance', model='config')
        self.assertEqual(six.text_type(ct), 'config')

    def test_linebreaks(self):
        self.client.login(username='admin', password='nimda')
        request = self.rf.get('/admin/constance/config/')
        request.user = self.superuser
        response = self.options.changelist_view(request, {})
        self.assertContains(response, 'LINEBREAK_VALUE')
        self.assertContains(response, linebreaksbr('eggs\neggs'))

    @mock.patch('constance.settings.CONFIG_FIELDSETS', {
        'Numbers': ('LONG_VALUE', 'INT_VALUE',),
        'Text': ('STRING_VALUE', 'UNICODE_VALUE'),
    })
    def test_fieldset_headers(self):
        self.client.login(username='admin', password='nimda')
        request = self.rf.get('/admin/constance/config/')
        request.user = self.superuser
        response = self.options.changelist_view(request, {})
        self.assertContains(response, '<h2>Numbers</h2>')
        self.assertContains(response, '<h2>Text</h2>')

    @mock.patch('constance.settings.CONFIG_FIELDSETS', {
        'Numbers': ('LONG_VALUE', 'INT_VALUE',),
    })
    def test_fieldset_ordering_1(self):
        """Ordering of inner list should be preserved"""
        self.client.login(username='admin', password='nimda')
        request = self.rf.get('/admin/constance/config/')
        request.user = self.superuser
        response = self.options.changelist_view(request, {})
        response.render()
        content_str = response.content.decode('utf-8')
        self.assertGreater(
            content_str.find('INT_VALUE'),
            content_str.find('LONG_VALUE')
        )

    @mock.patch('constance.settings.CONFIG_FIELDSETS', {
        'Numbers': ('INT_VALUE', 'LONG_VALUE', ),
    })
    def test_fieldset_ordering_2(self):
        """Ordering of inner list should be preserved"""
        self.client.login(username='admin', password='nimda')
        request = self.rf.get('/admin/constance/config/')
        request.user = self.superuser
        response = self.options.changelist_view(request, {})
        response.render()
        content_str = response.content.decode('utf-8')
        self.assertGreater(
            content_str.find('LONG_VALUE'),
            content_str.find('INT_VALUE')
        )

    def test_labels(self):
        self.assertEqual(type(self.model._meta.label), str)
        self.assertEqual(type(self.model._meta.label_lower), str)
