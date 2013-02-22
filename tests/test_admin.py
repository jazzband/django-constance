from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from constance.admin import Config


class TestAdmin(TestCase):
    model = Config

    def setUp(self):
        self.rf = RequestFactory()
        self.user = User.objects.create_superuser('admin', 'nimda', 'a@a.cz')
        self.options = admin.site._registry[self.model]
        self.client.login(username=self.user, password='nimda')

    def test_changelist(self):
        request = self.rf.get('/admin/constance/config/')
        response = self.options.changelist_view(request, {})
        self.assertEquals(response.status_code, 200)
