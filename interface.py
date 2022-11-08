from abc import ABC, abstractmethod
from typing import Dict, Tuple

class SportsBettingInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def read(self, data):
        ...

    # @abstractmethod
    # def update(self, data):
    #     ...

    # @abstractmethod
    # def delete(self, data):
    #     ...