from indicators.indicator import *
from game.settings import *
import pygame as pg

class AttackIndicator(Indicator):
    def __init__(self, game, entity):
        indicator = pg.image.load('images/indicators/attack.png')
        super().__init__(game, entity, indicator)
        
    def search_actions(self):
        self.actions_positions.clear()
        for entity in self.game.entities:
            if entity.can_attack(self.entity):
                self.actions_positions.append((entity.x, entity.y, entity.z - 1))
        
    def handle_action(self, x, y, z):
        enemy = self.game.map.get_entity(x, y, z + 1)
        self.entity.attack(enemy)
    
    def has_possible_actions(self):
        return len(self.actions_positions) > 0