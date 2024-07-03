from django.contrib import admin

from cheeseshop.apps.storage.models import Shelf
from cheeseshop.apps.storage.models import Supply

admin.site.register(Shelf)
admin.site.register(Supply)
