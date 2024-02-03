import pygame as pg
from abc import ABC, abstractmethod
from astra.game.common.settings import FONT_SIZE

class UIComponent(ABC):
    def __init__(self, game, x, y, width, height):
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.font = pg.font.Font(None, FONT_SIZE)

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass