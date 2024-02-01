from inventory.item import *

class LifePotion(Item):
    def __init__(self):
        super().__init__('Life Potion', 'Restores 10 health points.', 'health', 10)
    
    