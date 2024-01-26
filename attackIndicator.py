from indicator import *
from settings import *
from monster import *
import pygame as pg

class AttackIndicator(Indicator):
    def __init__(self, game, player):
        indicator = pg.image.load('images/indicators/attack.png')
        super().__init__(game, player, indicator)
        
    def show_actions(self):
        self.indicators.clear()
        for entity in self.game.entities:
            if isinstance(entity, Monster):
                dx, dy = entity.x - self.player.x, entity.y - self.player.y
                if abs(dx) <= self.player.range and abs(dy) <= self.player.range:
                    self.indicators.append((entity.x, entity.y, entity.z - 1))
        
    def draw(self):
        super().draw()
        
    def handle_action(self, x, y, z):
        self.player.attack(x, y, z)
        
    def handle_click(self, mouse_pos):
        super().handle_click(mouse_pos)
    
    def has_possible_actions(self):
        return len(self.indicators) > 0