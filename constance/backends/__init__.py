
class Backend(object):

    def get(self, key):
        """
        Get the key from the backend store and return it.
        Return None if not found.
        """
        raise NotImplementedError

    def set(self, key, value):
        """
        Add the value to the backend store given the key.
        """
        raise NotImplementedError

