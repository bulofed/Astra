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
    
    def use(self, entity):
        entity.apply_effect(self.effect)
        entity.inventory.remove_item(self)