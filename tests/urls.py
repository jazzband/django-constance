from django.contrib import admin
from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)
