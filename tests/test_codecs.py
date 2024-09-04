import uuid
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from decimal import Decimal
from unittest import TestCase

from constance.codecs import dumps
from constance.codecs import loads
from constance.codecs import register_type


class TestJSONSerialization(TestCase):
    def setUp(self):
        self.datetime = datetime(2023, 10, 5, 15, 30, 0)
        self.date = date(2023, 10, 5)
        self.time = time(15, 30, 0)
        self.decimal = Decimal('10.5')
        self.uuid = uuid.UUID('12345678123456781234567812345678')
        self.string = 'test'
        self.integer = 42
        self.float = 3.14
        self.boolean = True
        self.none = None
        self.timedelta = timedelta(days=1, hours=2, minutes=3)
        self.list = [1, 2, self.date]
        self.dict = {'key': self.date, 'key2': 1}

    def test_serializes_and_deserializes_default_types(self):
        self.assertEqual(dumps(self.datetime), '{"__type__": "datetime", "__value__": "2023-10-05T15:30:00"}')
        self.assertEqual(dumps(self.date), '{"__type__": "date", "__value__": "2023-10-05"}')
        self.assertEqual(dumps(self.time), '{"__type__": "time", "__value__": "15:30:00"}')
        self.assertEqual(dumps(self.decimal), '{"__type__": "decimal", "__value__": "10.5"}')
        self.assertEqual(dumps(self.uuid), '{"__type__": "uuid", "__value__": "12345678123456781234567812345678"}')
        self.assertEqual(dumps(self.string), '{"__type__": "default", "__value__": "test"}')
        self.assertEqual(dumps(self.integer), '{"__type__": "default", "__value__": 42}')
        self.assertEqual(dumps(self.float), '{"__type__": "default", "__value__": 3.14}')
        self.assertEqual(dumps(self.boolean), '{"__type__": "default", "__value__": true}')
        self.assertEqual(dumps(self.none), '{"__type__": "default", "__value__": null}')
        self.assertEqual(dumps(self.timedelta), '{"__type__": "timedelta", "__value__": 93780.0}')
        self.assertEqual(
            dumps(self.list),
            '{"__type__": "default", "__value__": [1, 2, {"__type__": "date", "__value__": "2023-10-05"}]}',
        )
        self.assertEqual(
            dumps(self.dict),
            '{"__type__": "default", "__value__": {"key": {"__type__": "date", "__value__": "2023-10-05"}, "key2": 1}}',
        )
        for t in (
            self.datetime,
            self.date,
            self.time,
            self.decimal,
            self.uuid,
            self.string,
            self.integer,
            self.float,
            self.boolean,
            self.none,
            self.timedelta,
            self.dict,
            self.list,
        ):
            self.assertEqual(t, loads(dumps(t)))

    def test_invalid_deserialization(self):
        with self.assertRaisesRegex(ValueError, 'Expecting value'):
            loads('THIS_IS_NOT_RIGHT')
        with self.assertRaisesRegex(ValueError, 'Invalid object'):
            loads('{"__type__": "THIS_IS_NOT_RIGHT", "__value__": "test", "THIS_IS_NOT_RIGHT": "THIS_IS_NOT_RIGHT"}')
        with self.assertRaisesRegex(ValueError, 'Unsupported type'):
            loads('{"__type__": "THIS_IS_NOT_RIGHT", "__value__": "test"}')

    def test_handles_unknown_type(self):
        class UnknownType:
            pass

        with self.assertRaisesRegex(TypeError, 'Object of type UnknownType is not JSON serializable'):
            dumps(UnknownType())

    def test_custom_type_serialization(self):
        class CustomType:
            def __init__(self, value):
                self.value = value

        register_type(CustomType, 'custom', lambda o: o.value, lambda o: CustomType(o))
        custom_data = CustomType('test')
        json_data = dumps(custom_data)
        self.assertEqual(json_data, '{"__type__": "custom", "__value__": "test"}')
        deserialized_data = loads(json_data)
        self.assertTrue(isinstance(deserialized_data, CustomType))
        self.assertEqual(deserialized_data.value, 'test')

    def test_register_known_type(self):
        with self.assertRaisesRegex(ValueError, 'Discriminator must be specified'):
            register_type(int, '', lambda o: o.value, lambda o: int(o))
        with self.assertRaisesRegex(ValueError, 'Type with discriminator default is already registered'):
            register_type(int, 'default', lambda o: o.value, lambda o: int(o))
        register_type(int, 'new_custom_type', lambda o: o.value, lambda o: int(o))
        with self.assertRaisesRegex(ValueError, 'Type with discriminator new_custom_type is already registered'):
            register_type(int, 'new_custom_type', lambda o: o.value, lambda o: int(o))

    def test_nested_collections(self):
        data = {'key': [[[[{'key': self.date}]]]]}
        self.assertEqual(
            dumps(data),
            (
                '{"__type__": "default", '
                '"__value__": {"key": [[[[{"key": {"__type__": "date", "__value__": "2023-10-05"}}]]]]}}'
            ),
        )
        self.assertEqual(data, loads(dumps(data)))
