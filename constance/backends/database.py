from constance.backends import Backend
from constance import settings, signals, config
from constance.models import Constance


class DatabaseBackend(Backend):

    def add_prefix(self, key):
        return "%s%s" % (settings.DATABASE_PREFIX, key)

    def mget(self, keys):
        if not keys:
            return {}

        objects = Constance.objects.filter(key__in=[self.add_prefix(key) for key in keys])
        # all keys should be present in result even they are absent in database
        result = {key: self.get_default(key) for key in keys}
        for obj in objects:
            result[obj.key] = obj.value
        return result

    def get(self, key):
        try:
            obj = Constance.objects.get(key=self.add_prefix(key))
            value = obj.value
        except Constance.DoesNotExist:
            value = None
        return value

    def set(self, key, value):
        db_key = self.add_prefix(key)

        try:
            obj = Constance.objects.get(key=db_key)
            old_value = obj.value
            if value == old_value:
                return
            else:
                obj.value = value
                obj.save()
        except Constance.DoesNotExist:
            old_value = self.get_default(key)
            Constance.objects.create(key=db_key, value=value)

        signals.config_updated.send(
            sender=config, key=key, old_value=old_value, new_value=value
        )
