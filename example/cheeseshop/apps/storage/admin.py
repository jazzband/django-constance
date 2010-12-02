from django.contrib import admin
from cheeseshop.apps.storage.models import Shelf, Supply

admin.site.register(Shelf)
admin.site.register(Supply)
