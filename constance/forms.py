import hashlib
from datetime import datetime, date, time
from decimal import Decimal

from django import forms
from django.contrib.admin import widgets
from django.core.exceptions import ImproperlyConfigured
from django.forms import fields
from django.utils import six
from django.utils.encoding import smart_bytes
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from . import config, settings
from .utils import get_constance_values


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


class ConstanceForm(forms.Form):
    version = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, initial, *args, **kwargs):
        super(ConstanceForm, self).__init__(*args, initial=initial, **kwargs)
        version_hash = hashlib.md5()

        for name, options in settings.CONFIG.items():
            default, help_text = options[0], options[1]
            if len(options) == 3:
                config_type = options[2]
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
        for name in settings.CONFIG:
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


def get_constance_field(name):
    form = ConstanceForm(initial=get_constance_values())

    return form.fields[name]


def set_constance_value(raw_name, raw_value):
    """
    Parses and sets a Constance value
    :param raw_name:
    :param raw_value:
    :return:
    """
    field = get_constance_field(raw_name)

    value = field.clean(field.to_python(raw_value))
    setattr(config, raw_name, value)
