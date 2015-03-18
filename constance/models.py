try:
    # available in Django 1.7+
    from django.db.models.signals import post_migrate
except ImportError:
    from django.db.models.signals import post_syncdb as post_migrate


def create_perm(*args, **kwargs):
    """
    Creates a fake content type and permission
    to be able to check for permissions
    """
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    if ContentType._meta.installed and Permission._meta.installed:
        content_type, created = ContentType.objects.get_or_create(
            #name='config',
            app_label='constance',
            model='config')

        permission, created = Permission.objects.get_or_create(
            #name='Can change config',
            content_type=content_type,
            codename='change_config')


post_migrate.connect(create_perm, dispatch_uid="constance.create_perm")
