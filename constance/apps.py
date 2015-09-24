from django.db.models import signals
from django import VERSION
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConstanceConfig(AppConfig):
    name = 'constance'
    verbose_name = _('Constance')

    def ready(self):
        super(ConstanceConfig, self).ready()
        signals.post_migrate.connect(self.create_perm,
                                     dispatch_uid='constance.create_perm')

    def create_perm(self, *args, **kwargs):
        """
        Creates a fake content type and permission
        to be able to check for permissions
        """
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        if ContentType._meta.installed and Permission._meta.installed:
            extra = {} if VERSION >= (1, 8) else {'name': 'config'}
            content_type, created = ContentType.objects.get_or_create(
                app_label='constance',
                model='config',
                **extra)

            permission, created = Permission.objects.get_or_create(
                name='Can change config',
                content_type=content_type,
                codename='change_config')
