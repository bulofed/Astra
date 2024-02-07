from abc import ABC, abstractmethod

class Object(ABC):
    def __init__(self, game, x, y, z):
        """The object class is the base class for all objects in the game.
        It contains the x, y, and z coordinates of the object, used to place it in the world."""
        self.game = game
        self.x = x
        self.y = y
        self.z = z
        
    @abstractmethod
    def draw(self):
        pass
    
    @abstractmethod
    def update(self):
        pass