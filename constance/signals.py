import django.dispatch

updated_signal = django.dispatch.Signal(providing_args=['key', 'value'])
