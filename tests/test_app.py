from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals
from django.test import TestCase


class TestApp(TestCase):
    def setUp(self):
        self.app_config = apps.get_app_config('constance')

    def test_post_migrate_signal_creates_content_type_and_permission_in_default_database(self):
        self.assert_uses_correct_database('default')

    def test_post_migrate_signal_creates_content_type_and_permission_in_secondary_database(self):
        self.assert_uses_correct_database('secondary')

    def test_uses_default_db_even_without_giving_using_keyword(self):
        self.call_post_migrate(None)

        self.assert_content_type_and_permission_created('default')

    def assert_uses_correct_database(self, database_name):
        self.call_post_migrate(database_name)

        self.assert_content_type_and_permission_created(database_name)

    def assert_content_type_and_permission_created(self, database_name):
        content_type_queryset = ContentType.objects.filter(app_label=self.app_config.name) \
            .using(database_name)

        self.assertTrue(content_type_queryset.exists())

        permission_queryset = Permission.objects.filter(content_type=content_type_queryset.get()) \
            .using(database_name).exists()

        self.assertTrue(permission_queryset)

    def call_post_migrate(self, database_name):
        signals.post_migrate.send(
            sender=self.app_config,
            app_config=self.app_config,
            verbosity=None,
            interactive=None,
            using=database_name
        )
