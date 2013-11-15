from datetime import datetime, date, time
from decimal import Decimal
from operator import itemgetter
import six

from django import forms
from django.contrib import admin, messages
from django.contrib.admin import widgets
from django.contrib.admin.options import csrf_protect_m
from django.core.exceptions import PermissionDenied
from django.forms import fields
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.formats import localize
from django.utils.translation import ugettext as _

try:
    from django.conf.urls import patterns, url
except ImportError:  # Django < 1.4
    from django.conf.urls.defaults import patterns, url


from constance import config, settings


NUMERIC_WIDGET = forms.TextInput(attrs={'size': 10})

INTEGER_LIKE = (fields.IntegerField, {'widget': NUMERIC_WIDGET})
STRING_LIKE = (fields.CharField, {
    'widget': forms.Textarea(attrs={'rows': 3}),
#    'required': False,
})

FIELDS = {
    bool: (fields.BooleanField, {'required': False}),
    int: INTEGER_LIKE,
    Decimal: (fields.DecimalField, {'widget': NUMERIC_WIDGET}),
    str: STRING_LIKE,
    datetime: (fields.DateTimeField, {'widget': widgets.AdminSplitDateTime}),
    date: (fields.DateField, {'widget': widgets.AdminDateWidget}),
    time: (fields.TimeField, {'widget': widgets.AdminTimeWidget}),
    float: (fields.FloatField, {'widget': NUMERIC_WIDGET}),
}

if not six.PY3:
    FIELDS.update({
        long: INTEGER_LIKE,
        unicode: STRING_LIKE,
    })


class ConstanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ConstanceForm, self).__init__(*args, **kwargs)
        for name, opts in settings.CONFIG.iteritems():
            _type = type(opts['default'])
            field_class, kwargs = FIELDS[_type]
            if _type in (str, unicode) and opts.get('required', True) is False:
                kwargs['required'] = False
            self.fields[name] = field_class(label=name, **kwargs)
            if settings.READONLY:
                self.fields[name].widget.attrs['disabled'] = 'disabled'

    def save(self):
        for name in self.cleaned_data:
            setattr(config, name, self.cleaned_data[name])


class ConstanceAdmin(admin.ModelAdmin):

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.module_name
        return patterns('',
            url(r'^$',
                self.admin_site.admin_view(self.changelist_view),
                name='%s_%s_changelist' % info),
            url(r'^$',
                self.admin_site.admin_view(self.changelist_view),
                name='%s_%s_add' % info),
        )

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        # First load a mapping between config name and default value
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        default_initial = ((name, opts['default'])
                           for name, opts in settings.CONFIG.iteritems())
        # Then update the mapping with actually values from the backend
        initial = dict(default_initial,
            **dict(config._backend.mget(settings.CONFIG.keys())))
        form = ConstanceForm(initial=initial)
        if request.method == 'POST':
            form = ConstanceForm(request.POST)
            if form.is_valid():
                form.save()
                # In django 1.5 this can be replaced with self.message_user
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _('Live settings updated successfully.'),
                )
                return HttpResponseRedirect('.')
        context = {
            'config': [],
            'title': _('Constance config'),
            'app_label': 'constance',
            'opts': Config._meta,
            'form': form,
            'media': self.media + form.media,
            'readonly': settings.READONLY,
        }
        for name, opts in settings.CONFIG.iteritems():
            default = opts['default']
            help_text = opts['help_text']
            # First try to load the value from the actual backend
            value = initial.get(name)
            # Then if the returned value is None, get the default
            if value is None:
                value = getattr(config, name)
            context['config'].append({
                'name': name,
                'default': localize(default),
                'help_text': _(help_text),
                'value': localize(value),
                'modified': value != default,
                'form_field': form[name],
            })
        context['config'].sort(key=itemgetter('name'))
        context_instance = RequestContext(request,
                                          current_app=self.admin_site.name)
        template_name = 'admin/constance/change_list.html'
        return render_to_response(template_name, context,
                                  context_instance=context_instance)

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def has_change_permission(self, request, obj=None):
        if settings.SUPERUSER_ONLY:
            return request.user.is_superuser
        return super(ConstanceAdmin, self).has_change_permission(request, obj)


class Config(object):
    class Meta(object):
        app_label = 'constance'
        object_name = 'Config'
        model_name = module_name = 'config'
        verbose_name_plural = 'config'
        get_ordered_objects = lambda x: False
        abstract = False
        swapped = False

        def get_change_permission(self):
            return 'change_%s' % self.model_name

    _meta = Meta()


admin.site.register([Config], ConstanceAdmin)
