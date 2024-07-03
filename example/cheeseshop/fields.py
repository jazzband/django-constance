import json

from django.forms import fields
from django.forms import widgets


class JsonField(fields.CharField):
    widget = widgets.Textarea

    def __init__(self, rows: int = 5, **kwargs):
        self.rows = rows
        super().__init__(**kwargs)

    def widget_attrs(self, widget: widgets.Widget):
        attrs = super().widget_attrs(widget)
        attrs['rows'] = self.rows
        return attrs

    def to_python(self, value):
        if value:
            return json.loads(value)
        return {}

    def prepare_value(self, value):
        return json.dumps(value)
