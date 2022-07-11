from django.db.models import signals
from django.apps import apps, AppConfig
from django.utils.translation import gettext_lazy as _


class ConstanceConfig(AppConfig):
    name = 'constance'
    verbose_name = _('Constance')

    def ready(self):
        super().ready()
        signals.post_migrate.connect(self.create_perm,
                                     dispatch_uid='constance.create_perm')

    def create_perm(self, using=None, *args, **kwargs):
        """
        Creates a fake content type and permission
        to be able to check for permissions
        """
        from django.conf import settings

        constance_dbs = getattr(settings, 'CONSTANCE_DBS', None)
        if constance_dbs is not None and using not in constance_dbs:
            return
        if (
            apps.is_installed('django.contrib.contenttypes') and
            apps.is_installed('django.contrib.auth')
        ):
            ContentType = apps.get_model('contenttypes.ContentType')
            Permission = apps.get_model('auth.Permission')
            content_type, created = ContentType.objects.using(using).get_or_create(
                app_label='constance',
                model='config',
            )

            Permission.objects.using(using).get_or_create(
                content_type=content_type,
                codename='change_config',
                defaults={'name': 'Can change config'},
            )
            Permission.objects.using(using).get_or_create(
                content_type=content_type,
                codename='view_config',
                defaults={'name': 'Can view config'},
            )
