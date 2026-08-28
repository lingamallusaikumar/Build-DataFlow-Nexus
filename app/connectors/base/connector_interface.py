from abc import ABC, abstractmethod

class BaseConnector(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def push_data(self, data):
        pass
        
    @abstractmethod
    def test_connection(self) -> bool:
        pass
