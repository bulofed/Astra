from inventory.item import *

class LifePotion(Item):
    def __init__(self):
        super().__init__('Life Potion', 'Restores 10 health points.', 'health', 10)
    
    def use(self, entity):
        entity.health += self.value
        entity.health = min(entity.health, entity.max_health)
        entity.inventory.remove_item(self)