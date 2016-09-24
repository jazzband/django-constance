from datetime import datetime, date, time
from decimal import Decimal

from django.utils import six
from django import forms
from django.contrib.admin import widgets
from django.forms import fields
from django.utils.module_loading import import_string

from . import settings

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
