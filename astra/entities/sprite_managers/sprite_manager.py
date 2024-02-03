from abc import ABC, abstractmethod
import pygame as pg # used in inherited classes

class SpriteManager(ABC):
    def __init__(self, entity):
        self.entity = entity
        self.sprite = None

    @abstractmethod
    def load_sprite(self):
        pass

    def blit_sprite(self):
        self.entity.game.screen.blit(self.sprite, (self.entity.x - self.entity.game.camera.x, self.entity.y - self.entity.game.camera.y))