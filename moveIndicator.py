from indicator import *
from settings import *
import pygame as pg

class MoveIndicator(Indicator):
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.indicator = pg.image.load('images/indicators/move.png')
        self.indicator_mask = pg.mask.from_surface(self.indicator)
        self.indicators = []

    def show_actions(self):
        self.indicators.clear()
        for dx in range(-self.player.speed, self.player.speed + 1):
            for dy in range(-self.player.speed, self.player.speed + 1):
                x, y, z = self.player.x + dx, self.player.y + dy, self.player.z - 1
                block = self.game.map.get_block(x, y, z)
                if block and block.solid:
                    self.indicators.append((x, y, z))

    def draw(self):
        for x, y, z in self.indicators:
            x_iso, y_iso = self.game.map.calculate_isometric_position(x, y, z, self.game.camera.zoom)
            indicator_resized = pg.transform.scale(self.indicator, (int(SPRITE_WIDTH * self.game.camera.zoom), int(SPRITE_HEIGHT * self.game.camera.zoom)))
            self.game.screen.blit(indicator_resized, (x_iso - self.game.camera.x, y_iso - self.game.camera.y))
            self.indicator_mask = pg.mask.from_surface(indicator_resized)
    
    def handle_click(self, mouse_pos):
        for x, y, z in self.indicators:
            x_iso, y_iso = self.game.map.calculate_isometric_position(x, y, z, self.game.camera.zoom)
            offset_x = mouse_pos[0] - (x_iso - self.game.camera.x)
            offset_y = mouse_pos[1] - (y_iso - self.game.camera.y)
            if self.indicator_mask.overlap_area(self.game.mouse_mask, (offset_x, offset_y)) > 0:
                self.player.move(x, y, z + 1)
                self.game.selected_player = None
                self.indicators.clear()