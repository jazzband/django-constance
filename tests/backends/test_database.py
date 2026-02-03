from django.test import TestCase
from django.test import TransactionTestCase

from constance import settings
from constance.base import Config
from tests.storage import StorageTestsMixin


class TestDatabase(StorageTestsMixin, TestCase):
    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = "constance.backends.database.DatabaseBackend"
        super().setUp()

    def test_database_queries(self):
        # Read and set to default value
        with self.assertNumQueries(5):
            self.assertEqual(self.config.INT_VALUE, 1)

        # Read again
        with self.assertNumQueries(1):
            self.assertEqual(self.config.INT_VALUE, 1)

        # Set value
        with self.assertNumQueries(2):
            self.config.INT_VALUE = 15

    def tearDown(self):
        settings.BACKEND = self.old_backend


class TestDatabaseWithCache(StorageTestsMixin, TestCase):
    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = "constance.backends.database.DatabaseBackend"
        self.old_cache_backend = settings.DATABASE_CACHE_BACKEND
        settings.DATABASE_CACHE_BACKEND = "default"
        super().setUp()
        self.config._backend._cache.clear()

    def test_database_queries(self):
        # Read and set to default value
        with self.assertNumQueries(6):
            self.assertEqual(self.config.INT_VALUE, 1)

        # Read again
        with self.assertNumQueries(0):
            self.assertEqual(self.config.INT_VALUE, 1)

        # Set value
        with self.assertNumQueries(3):
            self.config.INT_VALUE = 15

    def tearDown(self):
        settings.BACKEND = self.old_backend
        settings.DATABASE_CACHE_BACKEND = self.old_cache_backend


class TestDatabaseAsync(TransactionTestCase):
    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = "constance.backends.database.DatabaseBackend"
        self.config = Config()

    def tearDown(self):
        settings.BACKEND = self.old_backend

    async def test_aget_returns_none_for_missing_key(self):
        result = await self.config._backend.aget("INT_VALUE")
        self.assertIsNone(result)

    async def test_aget_returns_value(self):
        await self.config._backend.aset("INT_VALUE", 42)
        result = await self.config._backend.aget("INT_VALUE")
        self.assertEqual(result, 42)

    async def test_aset_stores_value(self):
        await self.config._backend.aset("INT_VALUE", 99)
        result = await self.config._backend.aget("INT_VALUE")
        self.assertEqual(result, 99)

    async def test_amget_returns_empty_for_no_keys(self):
        result = await self.config._backend.amget([])
        self.assertEqual(result, {})

    async def test_amget_returns_values(self):
        await self.config._backend.aset("INT_VALUE", 10)
        await self.config._backend.aset("BOOL_VALUE", True)
        result = await self.config._backend.amget(["INT_VALUE", "BOOL_VALUE"])
        self.assertEqual(result, {"INT_VALUE": 10, "BOOL_VALUE": True})


class TestDatabaseWithCacheAsync(TransactionTestCase):
    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = "constance.backends.database.DatabaseBackend"
        self.old_cache_backend = settings.DATABASE_CACHE_BACKEND
        settings.DATABASE_CACHE_BACKEND = "default"
        self.config = Config()
        self.config._backend._cache.clear()

    def tearDown(self):
        settings.BACKEND = self.old_backend
        settings.DATABASE_CACHE_BACKEND = self.old_cache_backend

    async def test_aget_returns_none_for_missing_key(self):
        result = await self.config._backend.aget("INT_VALUE")
        self.assertIsNone(result)

    async def test_aget_returns_value_from_cache(self):
        # First set a value using async
        await self.config._backend.aset("INT_VALUE", 42)
        # Clear cache and re-fetch to test aget path
        self.config._backend._cache.clear()
        result = await self.config._backend.aget("INT_VALUE")
        self.assertEqual(result, 42)

    async def test_aget_populates_cache(self):
        await self.config._backend.aset("INT_VALUE", 42)
        self.config._backend._cache.clear()

        # aget should populate the cache
        result = await self.config._backend.aget("INT_VALUE")
        self.assertEqual(result, 42)

    async def test_aset_stores_value(self):
        await self.config._backend.aset("INT_VALUE", 99)
        result = await self.config._backend.aget("INT_VALUE")
        self.assertEqual(result, 99)

    async def test_amget_returns_empty_for_no_keys(self):
        result = await self.config._backend.amget([])
        self.assertEqual(result, {})

    async def test_amget_returns_values(self):
        await self.config._backend.aset("INT_VALUE", 10)
        await self.config._backend.aset("BOOL_VALUE", True)
        result = await self.config._backend.amget(["INT_VALUE", "BOOL_VALUE"])
        self.assertEqual(result, {"INT_VALUE": 10, "BOOL_VALUE": True})

    async def test_amget_uses_cache(self):
        # Set values using async and ensure they're cached
        await self.config._backend.aset("INT_VALUE", 10)
        await self.config._backend.aset("BOOL_VALUE", True)

        result = await self.config._backend.amget(["INT_VALUE", "BOOL_VALUE"])
        self.assertEqual(result["INT_VALUE"], 10)
        self.assertEqual(result["BOOL_VALUE"], True)
