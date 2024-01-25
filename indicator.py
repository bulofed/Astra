from abc import ABC, abstractmethod

class Indicator(ABC):
    @abstractmethod
    def show_actions(self):
        pass

    @abstractmethod
    def draw(self):
        pass