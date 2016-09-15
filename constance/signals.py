import django.dispatch

config_updated = django.dispatch.Signal(
    providing_args=['updated_key', 'new_value']
)
