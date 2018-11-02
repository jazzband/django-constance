from django.forms import fields
from django.test import TransactionTestCase
import mock
import datetime

from constance.admin import ConstanceForm, get_values
from constance.management.commands.constance import _set_constance_value
from constance import config

class TestForm(TransactionTestCase):
    def setUp(self):
        self.initial_values = get_values()

    def test_form_field_types(self):

        f = ConstanceForm({})

        self.assertIsInstance(f.fields['INT_VALUE'], fields.IntegerField)
        self.assertIsInstance(f.fields['LONG_VALUE'], fields.IntegerField)
        self.assertIsInstance(f.fields['BOOL_VALUE'], fields.BooleanField)
        self.assertIsInstance(f.fields['STRING_VALUE'], fields.CharField)
        self.assertIsInstance(f.fields['UNICODE_VALUE'], fields.CharField)
        self.assertIsInstance(f.fields['DECIMAL_VALUE'], fields.DecimalField)
        self.assertIsInstance(f.fields['DATETIME_VALUE'], fields.SplitDateTimeField)
        self.assertIsInstance(f.fields['TIMEDELTA_VALUE'], fields.DurationField)
        self.assertIsInstance(f.fields['FLOAT_VALUE'], fields.FloatField)
        self.assertIsInstance(f.fields['DATE_VALUE'], fields.DateField)
        self.assertIsInstance(f.fields['TIME_VALUE'], fields.TimeField)

        # from CONSTANCE_ADDITIONAL_FIELDS
        self.assertIsInstance(f.fields['CHOICE_VALUE'], fields.ChoiceField)
        self.assertIsInstance(f.fields['EMAIL_VALUE'], fields.EmailField)

    def test_datetime_custom(self):
        initial_values = get_values()
        f = ConstanceForm(initial=initial_values)
        value = initial_values['DATETIME_VALUE']
        field = f.fields['DATETIME_VALUE']
        clean_value = field.clean(field.to_python((value.date(), value.time())))
        self.assertEqual(initial_values['DATETIME_VALUE'], clean_value)

    @mock.patch('constance.admin.ConstanceForm.clean_version', lambda x: 'test')
    def test_save(self):
        initial_values  = self.initial_values
        data = get_values().copy()
        data["version"] = 'test'
        now = datetime.datetime(2018, 1, 1, 23, 0, 0)
        data['DATETIME_VALUE_0'] = now.date()
        data['DATETIME_VALUE_1'] = now.time()
        del data['DATETIME_VALUE']
        f = ConstanceForm(initial=initial_values, data=data)
        self.assertTrue(f.is_valid(), msg=f.errors.as_data())
        f.save()
        self.assertEqual(f.cleaned_data['DATETIME_VALUE'], now)

    def tearDown(self):
        initial_values = self.initial_values
        values = (initial_values['DATETIME_VALUE'].date(),
                  initial_values['DATETIME_VALUE'].time())
        _set_constance_value('DATETIME_VALUE', values)



