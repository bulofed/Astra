from astra.objects.item.item_properties import ItemProperties
from astra.objects.item.effect import Effect

class LifePotion(ItemProperties):
    def __init__(self):
        super().__init__('Poison Potion', 'Make an enemy take 5HP per turn for 3 turns.', Effect('poison', 5, 3))