from django.forms import fields
from django.test import TestCase

from constance.forms import ConstanceForm


class TestForm(TestCase):
    def test_form_field_types(self):
        f = ConstanceForm({})

        self.assertIsInstance(f.fields['INT_VALUE'], fields.IntegerField)
        self.assertIsInstance(f.fields['BOOL_VALUE'], fields.BooleanField)
        self.assertIsInstance(f.fields['STRING_VALUE'], fields.CharField)
        self.assertIsInstance(f.fields['DECIMAL_VALUE'], fields.DecimalField)
        self.assertIsInstance(f.fields['DATETIME_VALUE'], fields.SplitDateTimeField)
        self.assertIsInstance(f.fields['TIMEDELTA_VALUE'], fields.DurationField)
        self.assertIsInstance(f.fields['FLOAT_VALUE'], fields.FloatField)
        self.assertIsInstance(f.fields['DATE_VALUE'], fields.DateField)
        self.assertIsInstance(f.fields['TIME_VALUE'], fields.TimeField)

        # from CONSTANCE_ADDITIONAL_FIELDS
        self.assertIsInstance(f.fields['CHOICE_VALUE'], fields.ChoiceField)
        self.assertIsInstance(f.fields['EMAIL_VALUE'], fields.EmailField)
