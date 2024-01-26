from indicator import *
from settings import *
import pygame as pg

class MoveIndicator(Indicator):
    def __init__(self, game, player):
        indicator = pg.image.load('images/indicators/move.png')
        super().__init__(game, player, indicator)

    def show_actions(self):
        self.indicators.clear()
        for dx, dy in itertools.product(range(-self.player.speed, self.player.speed + 1), range(-self.player.speed, self.player.speed + 1)):
            x, y, z = self.player.x + dx, self.player.y + dy, self.player.z - 1
            block = self.game.map.get_block(x, y, z)
            if block and block.solid and (x, y, z) not in self.player.attack_indicator.indicators:
                self.indicators.append((x, y, z))

    def draw(self):
        super().draw()
        
    def handle_action(self, x, y, z):
        self.player.move(x, y, z)
    
    def handle_click(self, mouse_pos):
        super().handle_click(mouse_pos)