from __future__ import absolute_import
from django import template
from django.conf import settings
from django.core.files.storage import get_storage_class

try:
    from django.contrib.staticfiles.storage import staticfiles_storage
except ImportError:
    staticfiles_storage = get_storage_class(settings.STATICFILES_STORAGE)()

register = template.Library()


@register.simple_tag
def static(path):
    """
    A template tag that returns the URL to a file
    using staticfiles' storage backend
    """
    return staticfiles_storage.url(path)
