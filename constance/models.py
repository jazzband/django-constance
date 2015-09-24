from django.db.models import signals
from django import VERSION


def create_perm(app, created_models, verbosity, db, **kwargs):
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


signals.post_syncdb.connect(create_perm, dispatch_uid="constance.create_perm")
