from abc import ABC, abstractmethod

class Entity(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass