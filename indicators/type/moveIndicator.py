from indicators.indicator import *
from game.settings import *
import pygame as pg

class MoveIndicator(Indicator):
    def __init__(self, game, entity):
        indicator = pg.image.load('images/indicators/move.png')
        super().__init__(game, entity, indicator)

    def search_actions(self):
        self.actions_positions.clear()
        for dx, dy, dz in itertools.product(range(-self.entity.speed, self.entity.speed + 1), 
                                            range(-self.entity.speed, self.entity.speed + 1), 
                                            range(-1, 2)):
            x, y, z = self.entity.x + dx, self.entity.y + dy, self.entity.z - 1 + dz
            block = self.game.map.get_block(x, y, z)
            block_above = self.game.map.get_block(x, y, z + 1)
            if block and block.solid and not block_above and not self.entity.is_position_occupied(x, y, z):
                self.actions_positions.append((x, y, z))
        
    def handle_action(self, x, y, z):
        self.entity.move(x, y, z + 1)