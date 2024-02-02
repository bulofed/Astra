import pygame as pg
from abc import ABC, abstractmethod
from game.settings import *

class Item(ABC):
    def __init__(self, name, description, effect, value):
        self.name = name
        self.description = description
        self.effect = effect
        self.value = value
        self.load_sprites()
        
    def load_sprites(self):
        self.sprite = pg.image.load(f'images/items/{self.name}.png')
    
    @abstractmethod
    def use(self, entity):
        pass