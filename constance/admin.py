from collections import OrderedDict
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from operator import itemgetter
import hashlib
import os

from django import forms, VERSION
from django.apps import apps
from django.conf import settings as django_settings
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin import widgets
from django.contrib.admin.options import csrf_protect_m
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.core.files.storage import default_storage
from django.forms import fields
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils import six
from django.utils.encoding import smart_bytes
from django.utils.formats import localize
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from . import LazyConfig, settings
from .checks import get_inconsistent_fieldnames


config = LazyConfig()


NUMERIC_WIDGET = forms.TextInput(attrs={'size': 10})

INTEGER_LIKE = (fields.IntegerField, {'widget': NUMERIC_WIDGET})
STRING_LIKE = (fields.CharField, {
    'widget': forms.Textarea(attrs={'rows': 3}),
    'required': False,
})

FIELDS = {
    bool: (fields.BooleanField, {'required': False}),
    int: INTEGER_LIKE,
    Decimal: (fields.DecimalField, {'widget': NUMERIC_WIDGET}),
    str: STRING_LIKE,
    datetime: (
        fields.SplitDateTimeField, {'widget': widgets.AdminSplitDateTime}
    ),
    timedelta: (
        fields.DurationField, {'widget': widgets.AdminTextInputWidget}
    ),
    date: (fields.DateField, {'widget': widgets.AdminDateWidget}),
    time: (fields.TimeField, {'widget': widgets.AdminTimeWidget}),
    float: (fields.FloatField, {'widget': NUMERIC_WIDGET}),
}


def parse_additional_fields(fields):
    for key in fields:
        field = list(fields[key])

        if len(field) == 1:
            field.append({})

        field[0] = import_string(field[0])

        if 'widget' in field[1]:
            klass = import_string(field[1]['widget'])
            field[1]['widget'] = klass(
                **(field[1].get('widget_kwargs', {}) or {})
            )

            if 'widget_kwargs' in field[1]:
                del field[1]['widget_kwargs']

        fields[key] = field

    return fields


FIELDS.update(parse_additional_fields(settings.ADDITIONAL_FIELDS))

if not six.PY3:
    FIELDS.update({
        long: INTEGER_LIKE,
        unicode: STRING_LIKE,
    })


def get_values():
    """
    Get dictionary of values from the backend
    :return:
    """

    # First load a mapping between config name and default value
    default_initial = ((name, options[0])
                       for name, options in settings.CONFIG.items())
    # Then update the mapping with actually values from the backend
    initial = dict(default_initial, **dict(config._backend.mget(settings.CONFIG)))

    return initial


class ConstanceForm(forms.Form):
    version = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, initial, *args, **kwargs):
        super(ConstanceForm, self).__init__(*args, initial=initial, **kwargs)
        version_hash = hashlib.md5()

        for name, options in settings.CONFIG.items():
            default = options[0]
            if len(options) == 3:
                config_type = options[2]
                if config_type not in settings.ADDITIONAL_FIELDS and not isinstance(default, config_type):
                    raise ImproperlyConfigured(_("Default value type must be "
                                                 "equal to declared config "
                                                 "parameter type. Please fix "
                                                 "the default value of "
                                                 "'%(name)s'.")
                                               % {'name': name})
            else:
                config_type = type(default)

            if config_type not in FIELDS:
                raise ImproperlyConfigured(_("Constance doesn't support "
                                             "config values of the type "
                                             "%(config_type)s. Please fix "
                                             "the value of '%(name)s'.")
                                           % {'config_type': config_type,
                                              'name': name})
            field_class, kwargs = FIELDS[config_type]
            self.fields[name] = field_class(label=name, **kwargs)

            version_hash.update(smart_bytes(initial.get(name, '')))
        self.initial['version'] = version_hash.hexdigest()

    def save(self):
        for file_field in self.files:
            file = self.cleaned_data[file_field]
            default_storage.save(file.name, file)
            self.cleaned_data[file_field] = file.name

        for name in settings.CONFIG:
            if getattr(config, name) != self.cleaned_data[name]:
                setattr(config, name, self.cleaned_data[name])

    def clean_version(self):
        value = self.cleaned_data['version']

        if settings.IGNORE_ADMIN_VERSION_CHECK:
            return value

        if value != self.initial['version']:
            raise forms.ValidationError(_('The settings have been modified '
                                          'by someone else. Please reload the '
                                          'form and resubmit your changes.'))
        return value

    def clean(self):
        cleaned_data = super(ConstanceForm, self).clean()

        if not settings.CONFIG_FIELDSETS:
            return cleaned_data

        if get_inconsistent_fieldnames():
            raise forms.ValidationError(_('CONSTANCE_CONFIG_FIELDSETS is missing '
                                          'field(s) that exists in CONSTANCE_CONFIG.'))

        return cleaned_data


class ConstanceAdmin(admin.ModelAdmin):
    change_list_template = 'admin/constance/change_list.html'
    change_list_form = ConstanceForm

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.module_name
        return [
            url(r'^$',
                self.admin_site.admin_view(self.changelist_view),
                name='%s_%s_changelist' % info),
            url(r'^$',
                self.admin_site.admin_view(self.changelist_view),
                name='%s_%s_add' % info),
        ]

    def get_config_value(self, name, options, form, initial):
        default, help_text = options[0], options[1]
        # First try to load the value from the actual backend
        value = initial.get(name)
        # Then if the returned value is None, get the default
        if value is None:
            value = getattr(config, name)
        config_value = {
            'name': name,
            'default': localize(default),
            'raw_default': default,
            'help_text': _(help_text),
            'value': localize(value),
            'modified': localize(value) != localize(default),
            'form_field': form[name],
            'is_date': isinstance(default, date),
            'is_datetime': isinstance(default, datetime),
            'is_checkbox': isinstance(form[name].field.widget, forms.CheckboxInput),
            'is_file': isinstance(form[name].field.widget, forms.FileInput),
        }

        return config_value

    def get_changelist_form(self, request):
        """
        Returns a Form class for use in the changelist_view.
        """
        # Defaults to self.change_list_form in order to preserve backward
        # compatibility
        return self.change_list_form

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        if not self.has_change_permission(request, None):
            raise PermissionDenied
        initial = get_values()
        form_cls = self.get_changelist_form(request)
        form = form_cls(initial=initial)
        if request.method == 'POST':
            form = form_cls(
                data=request.POST, files=request.FILES, initial=initial
            )
            if form.is_valid():
                form.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _('Live settings updated successfully.'),
                )
                return HttpResponseRedirect('.')
        context = dict(
            self.admin_site.each_context(request),
            config_values=[],
            title=self.model._meta.app_config.verbose_name,
            app_label='constance',
            opts=self.model._meta,
            form=form,
            media=self.media + form.media,
            icon_type='gif' if VERSION < (1, 9) else 'svg',
        )
        for name, options in settings.CONFIG.items():
            context['config_values'].append(
                self.get_config_value(name, options, form, initial)
            )

        if settings.CONFIG_FIELDSETS:
            context['fieldsets'] = []
            for fieldset_title, fields_list in settings.CONFIG_FIELDSETS.items():
                absent_fields = [field for field in fields_list
                                 if field not in settings.CONFIG]
                assert not any(absent_fields), (
                    "CONSTANCE_CONFIG_FIELDSETS contains field(s) that does "
                    "not exist: %s" % ', '.join(absent_fields))

                config_values = []

                for name in fields_list:
                    options = settings.CONFIG.get(name)
                    if options:
                        config_values.append(
                            self.get_config_value(name, options, form, initial)
                        )

                context['fieldsets'].append({
                    'title': fieldset_title,
                    'config_values': config_values
                })
            if not isinstance(settings.CONFIG_FIELDSETS, OrderedDict):
                context['fieldsets'].sort(key=itemgetter('title'))

        if not isinstance(settings.CONFIG, OrderedDict):
            context['config_values'].sort(key=itemgetter('name'))
        request.current_app = self.admin_site.name
        return TemplateResponse(request, self.change_list_template, context)

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
        verbose_name_plural = _('config')
        abstract = False
        swapped = False

        def get_ordered_objects(self):
            return False

        def get_change_permission(self):
            return 'change_%s' % self.model_name

        @property
        def app_config(self):
            return apps.get_app_config(self.app_label)

        @property
        def label(self):
            return '%s.%s' % (self.app_label, self.object_name)

        @property
        def label_lower(self):
            return '%s.%s' % (self.app_label, self.model_name)

    _meta = Meta()


admin.site.register([Config], ConstanceAdmin)
