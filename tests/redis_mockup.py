# Shared storage so sync (Connection) and async (AsyncConnection) instances
# operate on the same underlying data, just like a real Redis server would.
_shared_store = {}


class Connection:
    def set(self, key, value):
        _shared_store[key] = value

    def get(self, key, default=None):
        return _shared_store.get(key, default)

    def mget(self, keys):
        return [_shared_store.get(key) for key in keys]

    def clear(self):
        _shared_store.clear()


class AsyncConnection:
    async def set(self, key, value):
        _shared_store[key] = value

    async def get(self, key):
        return _shared_store.get(key)

    async def mget(self, keys):
        return [_shared_store.get(key) for key in keys]
