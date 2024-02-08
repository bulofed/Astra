import pygame as pg

class Indicator():
    def __init__(self, game, entity):
        self.game = game
        self.entity = entity
        self.entity_class = self.entity.__class__.__bases__[0].__bases__[0]