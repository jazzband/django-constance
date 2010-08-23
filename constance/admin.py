from datetime import datetime
from decimal import Decimal

from django.contrib import admin
from django.utils.functional import update_wrapper
from django.conf.urls.defaults import patterns, url
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.forms import fields
from django import forms

from constance import config



FIELDS = {
    bool: fields.BooleanField,
    int: fields.IntegerField,
    long: fields.IntegerField,
    Decimal: fields.DecimalField,
    str: fields.CharField,
    datetime: fields.DateTimeField,
    float: fields.FloatField,
}


class ConstanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ConstanceForm, self).__init__(*args, **kwargs)
        for name, (default, help_text) in settings.CONSTANCE_CONFIG.items():
            self.fields[name] = FIELDS[type(default)](label=name)

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
        }
        for name, (default, help_text) in settings.CONSTANCE_CONFIG.items():
            context['config'].append({
                'name': name,
                'default': default,
                'help_text': help_text,
                'value': getattr(config, name),
                'form_field': form[name]
            })

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
    _meta = Meta()


admin.site.register([Config], ConstanceAdmin)
