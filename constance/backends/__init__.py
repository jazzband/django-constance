"""Defines the base constance backend."""

from abc import ABC
from abc import abstractmethod


class Backend(ABC):
    @abstractmethod
    def get(self, key):
        """
        Get the key from the backend store and return the value.
        Return None if not found.
        """
        ...

    @abstractmethod
    async def aget(self, key):
        """
        Get the key from the backend store and return the value.
        Return None if not found.
        """
        ...

    @abstractmethod
    def mget(self, keys):
        """
        Get the keys from the backend store and return a list of the values.
        Return an empty list if not found.
        """
        ...

    @abstractmethod
    async def amget(self, keys):
        """
        Get the keys from the backend store and return a list of the values.
        Return an empty list if not found.
        """
        ...

    @abstractmethod
    def set(self, key, value):
        """Add the value to the backend store given the key."""
        ...

    @abstractmethod
    async def aset(self, key, value):
        """Add the value to the backend store given the key."""
        ...
