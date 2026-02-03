from django.test import TestCase
from django.test import TransactionTestCase

from constance import settings
from constance.base import Config
from tests.storage import StorageTestsMixin


class TestMemory(StorageTestsMixin, TestCase):
    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = "constance.backends.memory.MemoryBackend"
        super().setUp()
        self.config._backend._storage = {}

    def tearDown(self):
        self.config._backend._storage = {}
        settings.BACKEND = self.old_backend

    def test_mget_empty_keys(self):
        result = self.config._backend.mget([])
        self.assertIsNone(result)


class TestMemoryAsync(TransactionTestCase):
    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = "constance.backends.memory.MemoryBackend"
        self.config = Config()
        self.config._backend._storage = {}

    def tearDown(self):
        self.config._backend._storage = {}
        settings.BACKEND = self.old_backend

    async def test_aget_returns_none_for_missing_key(self):
        result = await self.config._backend.aget("INT_VALUE")
        self.assertIsNone(result)

    async def test_aget_returns_value(self):
        self.config._backend.set("INT_VALUE", 42)
        result = await self.config._backend.aget("INT_VALUE")
        self.assertEqual(result, 42)

    async def test_aset_stores_value(self):
        await self.config._backend.aset("INT_VALUE", 99)
        result = self.config._backend.get("INT_VALUE")
        self.assertEqual(result, 99)

    async def test_amget_returns_empty_for_no_keys(self):
        result = await self.config._backend.amget([])
        self.assertEqual(result, {})

    async def test_amget_returns_values(self):
        self.config._backend.set("INT_VALUE", 10)
        self.config._backend.set("BOOL_VALUE", True)
        result = await self.config._backend.amget(["INT_VALUE", "BOOL_VALUE"])
        self.assertEqual(result, {"INT_VALUE": 10, "BOOL_VALUE": True})
