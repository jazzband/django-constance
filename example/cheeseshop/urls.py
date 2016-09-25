from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
