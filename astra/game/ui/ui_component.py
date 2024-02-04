import pygame as pg
from abc import ABC, abstractmethod
from astra.game.common.settings import FONT_SIZE, WIDTH, HEIGHT

class UIComponent(ABC):
    def __init__(self, game, x, y):
        self.game = game
        self.rect = pg.Rect(x, y, WIDTH, HEIGHT)
        self.font = pg.font.SysFont("notosans", FONT_SIZE)
        self.color = (255, 255, 255)
        
    def draw_text(self, text, color=None, x=None, y=None):
        color = color if color is not None else self.color
        x = x if x is not None else self.rect.x
        y = y if y is not None else self.rect.y
        text_surface = self.font.render(text, True, color)
        self.game.screen.blit(text_surface, (x, y))

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self):
        pass