import itertools # used in child classes
from abc import ABC, abstractmethod
from game.settings import *
from game.utils import calculate_isometric_position
import pygame as pg

class Indicator(ABC):
    def __init__(self, game, entity, indicator):
        self.game = game
        self.entity = entity
        self.indicator = indicator
        self.indicator_mask = pg.mask.from_surface(self.indicator)
        self.actions_positions = []

    @abstractmethod
    def search_actions(self):
        pass

    def draw(self):
        for x, y, z in self.actions_positions:
            x_iso, y_iso = calculate_isometric_position(x, y, z, self.game.camera.zoom)
            indicator_resized = pg.transform.scale(self.indicator, (int(SPRITE_WIDTH * self.game.camera.zoom), int(SPRITE_HEIGHT * self.game.camera.zoom)))
            self.game.screen.blit(indicator_resized, (x_iso - self.game.camera.x, y_iso - self.game.camera.y))
            self.indicator_mask = pg.mask.from_surface(indicator_resized)
            
    @abstractmethod
    def handle_action(self, x, y, z):
        pass

    def handle_click(self, entity_manager, mouse_handler):
        for x, y, z in self.actions_positions:
            x_iso, y_iso = calculate_isometric_position(x, y, z, self.game.camera.zoom)
            offset_x = mouse_handler.mouse_x - (x_iso - self.game.camera.x)
            offset_y = mouse_handler.mouse_y - (y_iso - self.game.camera.y)
            if self.indicator_mask.overlap_area(mouse_handler.mouse_mask, (offset_x, offset_y)) > 0:
                self.handle_action(entity_manager, x, y, z)
                self.game.selected_player = None
    
    def is_clicked(self, mouse_handler):
        for x, y, z in self.actions_positions:
            x_iso, y_iso = calculate_isometric_position(x, y, z, self.game.camera.zoom)
            offset_x = mouse_handler.mouse_x - (x_iso - self.game.camera.x)
            offset_y = mouse_handler.mouse_y - (y_iso - self.game.camera.y)
            if self.indicator_mask.overlap_area(mouse_handler.mouse_mask, (offset_x, offset_y)) > 0:
                return True
        return False