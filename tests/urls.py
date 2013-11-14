from django.contrib import admin

try:
    from django.conf.urls import patterns, include
except ImportError:
    from django.conf.urls.defaults import patterns, include


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)
