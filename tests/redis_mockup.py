class Connection(dict):
    def set(self, key, value):
        self[key] = value

    def mget(self, keys):
        return [self.get(key) for key in keys]
