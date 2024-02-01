import pygame as pg
from game.settings import *

class Item:
    def __init__(self, name, description, effect, value):
        self.name = name
        self.description = description
        self.effect = effect
        self.value = value
        self.load_sprites()
        
    def load_sprites(self):
        self.sprite = pg.image.load(f'images/items/{self.name}.png')