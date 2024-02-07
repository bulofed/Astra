from abc import ABC, abstractmethod

class IEntitySpawner(ABC):
    def __init__(self, game):
        self.game = game
    
    @abstractmethod
    def spawn_entities(self):
        pass