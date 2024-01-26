import pygame as pg
from monster import *

class Goblin(Monster):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        self.speed = 1
        
    def load_sprites(self):
        self.sprites = []
        self.sprites.extend(
            pg.image.load(f'images/goblin/idle_d{i}.png') for i in range(1, 3)
        )
        
    def update(self):
        super().update()
        
    def draw(self):
        super().draw()