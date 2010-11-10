from operator import itemgetter
from time import time

from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.admin.options import csrf_protect_m
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.core.urlresolvers import reverse
from django.forms import fields
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.functional import update_wrapper
from django.utils.formats import localize
from django.utils.translation import ugettext_lazy as _

from constance import config


NUMERIC_WIDGET = forms.TextInput(attrs={'size': 10})

FIELDS = {
    bool: (fields.BooleanField, {'required': False}),
    int: (fields.IntegerField, {'widget': NUMERIC_WIDGET}),
    long: (fields.IntegerField, {'widget': NUMERIC_WIDGET}),
    Decimal: (fields.DecimalField, {'widget': NUMERIC_WIDGET}),
    str: (fields.CharField, {'widget': forms.TextInput(attrs={'size': 25})}),
    datetime: (fields.DateTimeField, {'widget': AdminSplitDateTime}),
    float: (fields.FloatField, {'widget': NUMERIC_WIDGET}),
}


class ConstanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ConstanceForm, self).__init__(*args, **kwargs)
        for name, (default, help_text) in settings.CONSTANCE_CONFIG.items():
            field_class, kwargs = FIELDS[type(default)]
            self.fields[name] = field_class(label=name, **kwargs)

    def save(self):
        for name in self.cleaned_data:
            setattr(config, name, self.cleaned_data[name])



class ConstanceAdmin(admin.ModelAdmin):

    @property
    def urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
        info = self.model._meta.app_label, self.model._meta.module_name
        urlpatterns = patterns('',
            url(r'^$',
                wrap(self.changelist_view),
                name='%s_%s_changelist' % info),
        )
        return urlpatterns

    def changelist_view(self, request):
        form = ConstanceForm(
            initial=dict( (name, getattr(config, name)) for name in settings.CONSTANCE_CONFIG)
        )
        if request.method == 'POST':
            form = ConstanceForm(request.POST)
            if form.is_valid():
                form.save()
                self.message_user(request, 'Live settings updated successfully.')
                return HttpResponseRedirect('#')
        context = {
            'config': [],
            'root_path': self.admin_site.root_path,
            'title': 'Live settings',
            'app_label': 'constance',
            'opts': Config._meta,
            'form': form,
            'media': self.media + form.media,
        }
        for name, (default, help_text) in settings.CONSTANCE_CONFIG.items():
            context['config'].append({
                'name': name,
                'default': default,
                'help_text': help_text,
                'value': getattr(config, name),
                'form_field': form[name]
            })
        context['config'].sort(key=itemgetter('name'))

        return render_to_response(
            'admin/constance/change_list.html',
            context,
            context_instance=RequestContext(request)
        )

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, *args, **kwargs):
        return True


class Config(object):
    class Meta(object):
        app_label = 'constance'
        module_name = 'config'
        verbose_name_plural = 'config'
        get_ordered_objects = lambda x: True
    _meta = Meta()


admin.site.register([Config], ConstanceAdmin)
