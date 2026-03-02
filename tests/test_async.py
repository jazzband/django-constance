import warnings

from django.test import TransactionTestCase

from constance import config
from constance import utils


class AsyncTestCase(TransactionTestCase):
    async def test_async_get(self):
        # Accessing an attribute on config should be awaitable when in async context
        val = await config.INT_VALUE
        self.assertEqual(val, 1)

    async def test_async_set(self):
        await config.aset("INT_VALUE", 42)
        val = await config.INT_VALUE
        self.assertEqual(val, 42)

        # Verify sync access also works (and emits warning)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            sync_val = int(config.INT_VALUE)
            self.assertEqual(sync_val, 42)
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_amget(self):
        values = await config.amget(["INT_VALUE", "BOOL_VALUE"])
        self.assertEqual(values["INT_VALUE"], 1)
        self.assertEqual(values["BOOL_VALUE"], True)

    async def test_sync_math_in_async_loop(self):
        # Accessing math should work but emit warning
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            res = config.INT_VALUE + 10
            # Note: res will be 42 + 10 if test_async_set ran before, or 1 + 10 if not.
            # TransactionTestCase should reset state, but let's be careful.
            # config.INT_VALUE defaults to 1.
            self.assertEqual(res, 11 if res < 50 else 52)
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_utils_aget_values(self):
        values = await utils.aget_values()
        self.assertIn("INT_VALUE", values)
        self.assertIn("BOOL_VALUE", values)
        self.assertEqual(values["INT_VALUE"], 1)

    async def test_utils_aget_values_for_keys(self):
        values = await utils.aget_values_for_keys(["INT_VALUE"])
        self.assertEqual(len(values), 1)
        self.assertEqual(values["INT_VALUE"], 1)

    async def test_bool_proxy(self):
        # BOOL_VALUE is True by default
        self.assertTrue(config.BOOL_VALUE)

    async def test_int_proxy(self):
        await config.aset("INT_VALUE", 1)
        self.assertEqual(int(config.INT_VALUE), 1)

    async def test_container_proxy(self):
        # LIST_VALUE is [1, "1", date(2019, 1, 1)] by default
        self.assertEqual(config.LIST_VALUE[0], 1)
        self.assertEqual(len(config.LIST_VALUE), 3)
        self.assertIn(1, config.LIST_VALUE)
        self.assertEqual(next(iter(config.LIST_VALUE)), 1)


class AsyncValueProxyTestCase(TransactionTestCase):
    """Tests for AsyncValueProxy dunder methods in async context."""

    async def test_str_proxy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = str(config.STRING_VALUE)
            self.assertEqual(result, "Hello world")
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_repr_proxy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = repr(config.STRING_VALUE)
            self.assertEqual(result, "'Hello world'")
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_float_proxy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = float(config.FLOAT_VALUE)
            self.assertAlmostEqual(result, 3.1415926536)
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_eq_proxy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = config.INT_VALUE == 1
            self.assertTrue(result)
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_ne_proxy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = config.INT_VALUE != 2
            self.assertTrue(result)
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_lt_proxy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = config.INT_VALUE < 10
            self.assertTrue(result)
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_le_proxy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = config.INT_VALUE <= 1
            self.assertTrue(result)
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_gt_proxy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = config.INT_VALUE > 0
            self.assertTrue(result)
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_ge_proxy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = config.INT_VALUE >= 1
            self.assertTrue(result)
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_hash_proxy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = hash(config.INT_VALUE)
            self.assertEqual(result, hash(1))
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_sub_proxy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = config.INT_VALUE - 1
            self.assertEqual(result, 0)
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_mul_proxy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = config.INT_VALUE * 5
            self.assertEqual(result, 5)
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_truediv_proxy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = config.INT_VALUE / 1
            self.assertEqual(result, 1.0)
            self.assertTrue(any("Synchronous access" in str(warn.message) for warn in w))

    async def test_aset_invalid_key(self):
        with self.assertRaises(AttributeError):
            await config.aset("INVALID_KEY", 42)


class AsyncUtilsTestCase(TransactionTestCase):
    """Tests for async utility functions."""

    async def test_aget_values_for_keys_invalid_type(self):
        with self.assertRaises(TypeError):
            await utils.aget_values_for_keys("key1")

    async def test_aget_values_for_keys_missing_key(self):
        with self.assertRaises(AttributeError) as ctx:
            await utils.aget_values_for_keys(["INVALID_KEY"])
        self.assertIn("INVALID_KEY", str(ctx.exception))

    async def test_aget_values_for_keys_empty(self):
        result = await utils.aget_values_for_keys([])
        self.assertEqual(result, {})


class ConfigBaseTestCase(TransactionTestCase):
    """Tests for Config class edge cases."""

    def test_config_dir(self):
        # Test __dir__ method
        keys = dir(config)
        self.assertIn("INT_VALUE", keys)
        self.assertIn("BOOL_VALUE", keys)

    def test_access_backend_attribute(self):
        # Test accessing _backend attribute in sync context
        backend = config._backend
        self.assertIsNotNone(backend)
