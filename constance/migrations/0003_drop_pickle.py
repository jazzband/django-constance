import logging
import pickle
from base64 import b64decode
from importlib import import_module

from django.db import migrations

from constance import settings
from constance.codecs import dumps

logger = logging.getLogger(__name__)


def import_module_attr(path):
    package, module = path.rsplit('.', 1)
    return getattr(import_module(package), module)


def migrate_pickled_data(apps, schema_editor) -> None:  # pragma: no cover
    Constance = apps.get_model('constance', 'Constance')

    for constance in Constance.objects.exclude(value=None):
        constance.value = dumps(pickle.loads(b64decode(constance.value.encode())))  # noqa: S301
        constance.save(update_fields=['value'])

    if settings.BACKEND in ('constance.backends.redisd.RedisBackend', 'constance.backends.redisd.CachingRedisBackend'):
        import redis

        _prefix = settings.REDIS_PREFIX
        connection_cls = settings.REDIS_CONNECTION_CLASS
        if connection_cls is not None:
            _rd = import_module_attr(connection_cls)()
        else:
            if isinstance(settings.REDIS_CONNECTION, str):
                _rd = redis.from_url(settings.REDIS_CONNECTION)
            else:
                _rd = redis.Redis(**settings.REDIS_CONNECTION)
        redis_migrated_data = {}
        for key in settings.CONFIG:
            prefixed_key = f'{_prefix}{key}'
            value = _rd.get(prefixed_key)
            if value is not None:
                try:
                    redis_migrated_data[prefixed_key] = dumps(pickle.loads(value))  # noqa: S301
                except pickle.UnpicklingError as e:
                    if value.startswith(b'{"__'):
                        # Seems like we're facing already migrated data
                        # Might be related to defaults and when config was accessed while django inits for migration
                        continue
                    raise e
        for prefixed_key, value in redis_migrated_data.items():
            _rd.set(prefixed_key, value)


class Migration(migrations.Migration):
    dependencies = [('constance', '0002_migrate_from_old_table')]

    operations = [
        migrations.RunPython(migrate_pickled_data),
    ]
