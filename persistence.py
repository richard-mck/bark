"""Managing persistence across different implementations"""

from abc import ABC, abstractmethod


class PersistenceLayer(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def create(self, data):
        raise NotImplementedError

    @abstractmethod
    def list(self, order_by):
        raise NotImplementedError

    @abstractmethod
    def edit(self, bookmark_id, data):
        raise NotImplementedError

    @abstractmethod
    def delete(self, bookmark_id):
        raise NotImplementedError
