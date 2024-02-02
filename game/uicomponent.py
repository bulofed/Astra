import pygame as pg
from game.settings import *

class UIComponent:
    def __init__(self, game, x, y, width, height):
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.font = pg.font.Font(None, FONT_SIZE)

    def draw(self):
        pass

    def update(self):
        pass