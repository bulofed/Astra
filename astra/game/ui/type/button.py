from abc import ABC, abstractmethod

class Button(ABC):
    def __init__(self, x, y, action=None):
        self.x = x
        self.y = y
        self.action = action

    @abstractmethod
    def draw(self, win):
        pass
    
    @abstractmethod
    def hover(self, pos):
        pass

    def click(self):
        if self.action is not None:
            self.action()