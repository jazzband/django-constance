from django.db.models import signals


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
            model='config')

        permission, created = Permission.objects.get_or_create(
            name='Can change config',
            content_type=content_type,
            codename='change_config')


if hasattr(signals, 'post_syncdb'):
    signals.post_syncdb.connect(create_perm, dispatch_uid="constance.create_perm")
else:
    signals.post_migrate.connect(create_perm, dispatch_uid="constance.create_perm")
