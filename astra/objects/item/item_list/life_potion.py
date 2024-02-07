from astra.objects.item.item_properties import ItemProperties

class LifePotion(ItemProperties):
    def __init__(self):
        super().__init__('Life Potion', 'Restores 10 health points.', 'health', 10)
    
    def use(self, entity):
        entity.heal(self.value)
        entity.inventory.remove_item(self)