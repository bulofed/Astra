import pygame as pg
from abc import ABC, abstractmethod

class ItemProperties(ABC):
    def __init__(self, name, description, effect, value):
        self.name = name
        self.description = description
        self.effect = effect
        self.value = value
        self.load_sprites()
        
    def load_sprites(self):
        name = self.__class__.__name__.lower()
        self.sprite = pg.image.load(f'astra/assets/images/items/{name}.png')
    
    @abstractmethod
    def use(self, entity):
        pass