import django.dispatch

config_updated = django.dispatch.Signal(
    providing_args=['key', 'old_value', 'new_value']
)
