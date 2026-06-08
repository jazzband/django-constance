from django.test import TestCase
from django.test import TransactionTestCase

from constance import LazyConfig
from constance import settings
from constance.backends.database import DatabaseBackend
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


class TestDatabaseBackendConstruction(TestCase):
    """Regression tests for #667: backend construction must not perform I/O."""

    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = "constance.backends.database.DatabaseBackend"

    def tearDown(self):
        settings.BACKEND = self.old_backend

    def test_backend_init_does_no_queries(self):
        with self.assertNumQueries(0):
            DatabaseBackend()

    def test_autofill_is_noop_without_cache(self):
        backend = DatabaseBackend()
        with self.assertNumQueries(0):
            backend.autofill()

    def test_backend_init_does_no_queries_with_cache(self):
        old_cache_backend = settings.DATABASE_CACHE_BACKEND
        settings.DATABASE_CACHE_BACKEND = "default"
        try:
            with self.assertNumQueries(0):
                DatabaseBackend()
        finally:
            settings.DATABASE_CACHE_BACKEND = old_cache_backend


class TestDatabaseAsync(TransactionTestCase):
    def setUp(self):
        self.old_backend = settings.BACKEND
        settings.BACKEND = "constance.backends.database.DatabaseBackend"
        self.config = Config()

    async def test_lazy_config_first_access_in_async(self):
        # End-to-end: LazyConfig _setup() runs from inside the loop and the
        # awaited value resolves. Companion to TestDatabaseBackendConstruction
        # which is the strict #667 regression test.
        lazy = LazyConfig()
        value = await lazy.INT_VALUE
        self.assertEqual(value, 1)

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
        await self.config._backend.aset("BOOL_VALUE", value=True)
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
        await self.config._backend.aset("BOOL_VALUE", value=True)
        result = await self.config._backend.amget(["INT_VALUE", "BOOL_VALUE"])
        self.assertEqual(result, {"INT_VALUE": 10, "BOOL_VALUE": True})

    async def test_amget_uses_cache(self):
        # Set values using async and ensure they're cached
        await self.config._backend.aset("INT_VALUE", 10)
        await self.config._backend.aset("BOOL_VALUE", value=True)

        result = await self.config._backend.amget(["INT_VALUE", "BOOL_VALUE"])
        self.assertEqual(result["INT_VALUE"], 10)
        self.assertEqual(result["BOOL_VALUE"], True)
