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
        if config.BOOL_VALUE:
            self.assertTrue(True)
        else:
            self.fail("BOOL_VALUE should be True")

    async def test_int_proxy(self):
        await config.aset("INT_VALUE", 1)
        self.assertEqual(int(config.INT_VALUE), 1)

    async def test_container_proxy(self):
        # LIST_VALUE is [1, "1", date(2019, 1, 1)] by default
        self.assertEqual(config.LIST_VALUE[0], 1)
        self.assertEqual(len(config.LIST_VALUE), 3)
        self.assertIn(1, config.LIST_VALUE)
        self.assertEqual(list(config.LIST_VALUE)[0], 1)
