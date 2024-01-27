from indicator import *
from settings import *
import pygame as pg

class AttackIndicator(Indicator):
    def __init__(self, game, entity):
        indicator = pg.image.load('images/indicators/attack.png')
        super().__init__(game, entity, indicator)
        
    def search_actions(self):
        self.indicators.clear()
        for entity in self.game.entities:
            if entity.can_attack(self.entity):
                self.indicators.append((entity.x, entity.y, entity.z - 1))
        
    def handle_action(self, x, y, z):
        entity = self.game.map.get_entity(x, y, z)
        self.entity.attack(entity)
    
    def has_possible_actions(self):
        return len(self.indicators) > 0