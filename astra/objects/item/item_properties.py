import pygame as pg

class ItemProperties():
    def __init__(self, name, description, effect):
        self.name = name
        self.description = description
        self.effect = effect
        self.load_sprites()
        
    def load_sprites(self):
        name = self.__class__.__name__.lower()
        self.sprite = pg.image.load(f'astra/assets/images/items/{name}.png')
    
    def use(self, entity, target=None):
        if target is not None:
            target.apply_effect(self.effect)
        else:
            entity.apply_effect(self.effect)
        entity.inventory.use_item(self)