from indicator import *
from settings import *
import pygame as pg

class MoveIndicator(Indicator):
    def __init__(self, game, entity):
        indicator = pg.image.load('images/indicators/move.png')
        super().__init__(game, entity, indicator)

    def search_actions(self):
        self.indicators.clear()
        for dx, dy in itertools.product(range(-self.entity.speed, self.entity.speed + 1), range(-self.entity.speed, self.entity.speed + 1)):
            x, y, z = self.entity.x + dx, self.entity.y + dy, self.entity.z - 1
            block = self.game.map.get_block(x, y, z)
            if block and block.solid and not self.entity.is_position_occupied(x, y, z):
                self.indicators.append((x, y, z))
        
    def handle_action(self, x, y, z):
        self.entity.move(x, y, z)