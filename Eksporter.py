from abc import ABC, abstractmethod

class Eksporter(ABC):
    @abstractmethod
    def eksportuj(self, dane):
        pass
