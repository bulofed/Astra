from entity import *

class Monster(Entity):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        
    @abstractmethod
    def load_sprites(self):
        pass

    @abstractmethod
    def update(self):
        super().update()
    
    @abstractmethod
    def draw(self):
        super().draw()