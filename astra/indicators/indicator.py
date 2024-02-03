from abc import ABC, abstractmethod
from astra.game.common.settings import SPRITE_WIDTH, SPRITE_HEIGHT
from astra.game.common.utils import calculate_isometric_position
from astra.game.position import Position
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
    
    def _calculate_offset(self, mouse_handler, x_iso, y_iso):
        offset_x = mouse_handler.mouse_x - (x_iso - self.game.camera.x)
        offset_y = mouse_handler.mouse_y - (y_iso - self.game.camera.y)
        return offset_x, offset_y

    def _is_overlap(self, mouse_handler, offset_x, offset_y):
        return self.indicator_mask.overlap_area(mouse_handler.mouse_mask, (offset_x, offset_y)) > 0

    def _handle_mouse_interaction(self, mouse_handler, position, action):
        offset_x, offset_y = self._calculate_offset(mouse_handler, position.x_iso, position.y_iso)
        if self._is_overlap(mouse_handler, offset_x, offset_y):
            action(position)

    def _iterate_actions_positions(self, mouse_handler, action):
        for x, y, z in self.actions_positions:
            x_iso, y_iso = calculate_isometric_position(x, y, z, self.game.camera.zoom)
            position = Position(x, y, z, x_iso, y_iso)
            if mouse_handler is not None:
                self._handle_mouse_interaction(mouse_handler, position, action)
            else:
                action(position)

    def draw(self):
        indicator_resized = pg.transform.scale(
            self.indicator,
            (int(SPRITE_WIDTH * self.game.camera.zoom), int(SPRITE_HEIGHT * self.game.camera.zoom))
        )
        self.indicator_mask = pg.mask.from_surface(indicator_resized)
        
        def blit_indicator(position):
            self.game.screen.blit(
                indicator_resized,
                (position.x_iso - self.game.camera.x, position.y_iso - self.game.camera.y)
            )
    
        self._iterate_actions_positions(None, blit_indicator)

            
    @abstractmethod
    def handle_action(self, x, y, z):
        pass

    def handle_click(self, entity_manager, mouse_handler):
        def action(position):
            self.handle_action(entity_manager, position.x, position.y, position.z)
        self._iterate_actions_positions(mouse_handler, action)
        self.game.selected_player = None