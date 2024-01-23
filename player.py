from settings import *
import pygame as pg

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y, self.z = PLAYER_POS
        
    def movement(self):
        dx, dy, dz = 0, 0, 0
        
        keys = pg.key.get_just_pressed()
        if keys[pg.K_LEFT]:
            dx -= 1
        elif keys[pg.K_RIGHT]:
            dx += 1
        elif keys[pg.K_UP]:
            dy -= 1
        elif keys[pg.K_DOWN]:
            dy += 1
        elif keys[pg.K_SPACE]:
            dz += 1
        elif keys[pg.K_LCTRL]:
            dz -= 1
    
        self.x += dx
        self.y += dy
        self.z += dz
        
    def update(self):
        self.movement()
            
    def draw(self):
        x, y = self.game.map.calculate_isometric_position(self.x, self.y, self.z, self.game.camera.zoom)
        pg.draw.circle(self.game.screen, 'red', (x - self.game.camera.x, y - self.game.camera.y), 10)
        
    @property
    def position(self):
        return self.x, self.y, self.z
    
    @property
    def tile_position(self):
        return self.x // TILE_WIDTH, self.y // TILE_HEIGHT, self.z