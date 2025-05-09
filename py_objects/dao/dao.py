# TODO: Design the DAO Object here
from abc import ABC, abstractmethod
from typing import Any

class DataAccessObject(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def search(self, key: str | int):
        pass

    @abstractmethod
    def create(self, item: Any):
        pass

    @abstractmethod
    def retrieve(self, search_string):
        pass

    # @abstractmethod
    # def update(self, **kwargs):
    #     pass

    # @abstractmethod
    # def delete(self, key):
    #     pass

    @abstractmethod
    def list_items(self):
        pass

    # @abstractmethod
    # def load(self):
    #     pass

    # @abstractmethod
    # def save(self):
    #     pass

