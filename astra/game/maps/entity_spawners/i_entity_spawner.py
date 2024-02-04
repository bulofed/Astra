from abc import ABC, abstractmethod

class IEntitySpawner(ABC):
    def __init__(self, game):
        self.game = game
        self.entities = []
        self.items = []
    
    @abstractmethod
    def spawn_entities(self):
        pass