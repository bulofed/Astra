from astra.game.common.settings import SPRITE_WIDTH, SPRITE_HEIGHT
from astra.game.common.utils import calculate_isometric_position
from astra.objects.object import Object
import pygame as pg

class IndicatorObject(Object):
    def __init__(self, game, entity, x, y, z, indicator):
        super().__init__(game, x, y, z)
        self.entity = entity
        self.indicator = indicator
        self.indicator_mask = pg.mask.from_surface(indicator)

    def draw(self, camera):
        indicator_resized = pg.transform.scale(
            self.indicator,
            (int(SPRITE_WIDTH * camera.zoom), int(SPRITE_HEIGHT * camera.zoom))
        )
        self.indicator_mask = pg.mask.from_surface(indicator_resized)
    
        x_iso, y_iso = calculate_isometric_position(self.x, self.y, self.z, camera.zoom)
        
        self.game.screen.blit(indicator_resized, (x_iso - camera.x, y_iso - camera.y))
        
    def update(self):
        pass