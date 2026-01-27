class Connection(dict):
    def set(self, key, value):
        self[key] = value

    async def aset(self, key, value):
        # Keep this for backward compatibility with previous commit if needed
        self.set(key, value)

    def get(self, key, default=None):
        return super().get(key, default)

    async def aget(self, key):
        # Keep this for backward compatibility
        return self.get(key)

    def mget(self, keys):
        return [self.get(key) for key in keys]

    async def amget(self, keys):
        # Keep this for backward compatibility
        return self.mget(keys)


class AsyncConnection(Connection):
    async def set(self, key, value):
        super().set(key, value)

    async def get(self, key):
        return super().get(key)

    async def mget(self, keys):
        return super().mget(keys)
