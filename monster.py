from entity import *
from attackIndicator import *
from moveIndicator import *

class Monster(Entity):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        self.attack_indicator = AttackIndicator(self.game, self)
        self.move_indicator = MoveIndicator(self.game, self)
        
    @abstractmethod
    def random_action(self):
        pass
    
    def can_attack(self, entity):
        return super().can_attack(entity, Monster)