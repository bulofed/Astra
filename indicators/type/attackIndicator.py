from indicators.indicator import *
from game.settings import *
from game.utils import get_entity
import pygame as pg

class AttackIndicator(Indicator):
    def __init__(self, game, entity):
        indicator = pg.image.load('images/indicators/attack.png')
        super().__init__(game, entity, indicator)

    def search_actions(self, entities):
        self.actions_positions = [(entity.x, entity.y, entity.z - 1) for entity in entities if entity.can_attack(self.entity)]

    def handle_action(self, entity_manager, x, y, z):
        enemy = get_entity(entity_manager.entities, x, y, z + 1)
        self.entity.attack(entity_manager, enemy)

    def has_possible_actions(self):
        return bool(self.actions_positions)