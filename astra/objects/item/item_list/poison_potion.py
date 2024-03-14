from astra.objects.item.types.target_item import TargetItem
from astra.objects.item.effect import Effect

class PoisonPotion(TargetItem):
    def __init__(self):
        super().__init__('Poison Potion', 'Make an enemy take 5HP per turn for 3 turns.', Effect('poison', 5, 3))