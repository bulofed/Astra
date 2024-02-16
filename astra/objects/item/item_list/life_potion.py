from astra.objects.item.types.self_item import SelfItem
from astra.objects.item.effect import Effect

class LifePotion(SelfItem):
    def __init__(self):
        super().__init__('Life Potion', 'Restores 10 health points.', Effect('heal', 10))