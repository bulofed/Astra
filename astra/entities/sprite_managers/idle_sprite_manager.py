from .sprite_manager import SpriteManager
import pygame as pg

class ItemSpriteManager(SpriteManager):
    def load_sprite(self):
        self.sprite = pg.image.load(f'images/items/{self.entity.name}.png')