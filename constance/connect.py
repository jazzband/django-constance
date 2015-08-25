import django
from django.db.models.signals import post_migrate

if django.VERSION >= (1, 8):
    CONTENT_TYPE_EXTRA = {}
else:
    CONTENT_TYPE_EXTRA = {'name': 'config'}

def create_perm(*args, **kwargs):
    """
    Creates a fake content type and permission
    to be able to check for permissions
    """
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    if ContentType._meta.installed and Permission._meta.installed:
        content_type, created = ContentType.objects.get_or_create(
            app_label='constance',
            model='config',
            **CONTENT_TYPE_EXTRA)

        permission, created = Permission.objects.get_or_create(
            name='Can change config',
            content_type=content_type,
            codename='change_config')


post_migrate.connect(create_perm, dispatch_uid="constance.create_perm")
