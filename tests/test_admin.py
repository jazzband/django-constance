from django.contrib import admin
from django.contrib.auth.models import User, Permission
from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory

from constance.admin import settings, Config


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
