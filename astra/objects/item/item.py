from astra.objects.object import Object
from astra.game.common.utils import calculate_isometric_position
import pygame as pg

class Item(Object):
    def __init__(self, game, x, y, z, properties):
        super().__init__(game, x, y, z)
        self.properties = properties
        
    def draw(self, camera):
        x, y = calculate_isometric_position(self.x, self.y, self.z, camera.zoom)
        zoomed_item = pg.transform.scale(self.properties.sprite, (int(16 * camera.zoom), int(16 * camera.zoom)))
        self.game.screen.blit(zoomed_item, (x - camera.x, y - camera.y))
    
    def update(self):
        pass