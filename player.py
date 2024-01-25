from settings import *
import pygame as pg

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y, self.z = PLAYER_POS
        self.current_frame = 0
        self.animation_time = 0
        self.frame_duration = .5
        self.speed = 1
        self.load_sprites()
    
    def load_sprites(self):
        self.sprites = []
        self.sprites.extend(
            pg.image.load(f'images/player/idle_d{i}.png') for i in range(1, 3)
        )
        
    def movement(self):
        dx, dy, dz = 0, 0, 0
        
        keys = pg.key.get_just_pressed()
        if keys[pg.K_LEFT]:
            dx += 1
        elif keys[pg.K_RIGHT]:
            dx -= 1
        elif keys[pg.K_UP]:
            dy -= 1
        elif keys[pg.K_DOWN]:
            dy += 1
        elif keys[pg.K_SPACE]:
            dz += 1
        elif keys[pg.K_LSHIFT]:
            dz -= 1
    
        self.x += dx
        self.y += dy
        self.z += dz
        
    def update(self):
        self.movement()
        self.animation_time += self.game.delta / 1000
        if self.animation_time >= self.frame_duration:
            self.animation_time -= self.frame_duration
            self.current_frame = (self.current_frame + 1) % len(self.sprites)
            
    def draw(self):
        self.x_iso, self.y_iso = self.game.map.calculate_isometric_position(self.x, self.y, self.z, self.game.camera.zoom)
        sprite = self.sprites[self.current_frame]
        sprite_resized = pg.transform.scale(sprite, (int(SPRITE_WIDTH * self.game.camera.zoom), int(SPRITE_HEIGHT * self.game.camera.zoom)))
        self.game.screen.blit(sprite_resized, (self.x_iso - self.game.camera.x, self.y_iso - self.game.camera.y))
        self.entity_rect = pg.Rect(self.x_iso, self.y_iso, SPRITE_WIDTH * self.game.camera.zoom, SPRITE_HEIGHT * self.game.camera.zoom)
    
    def show_actions(self):
        for dx in range(-self.speed, self.speed + 1):
            for dy in range(-self.speed, self.speed + 1):
                x, y, z = self.x + dx, self.y + dy, self.z - 1
                block = self.game.map.get_block(x, y, z)
                if block and block.solid:
                    print(f"Can move to block at ({x}, {y}, {z})")
        
    @property
    def position(self):
        return self.x, self.y, self.z
    
    @property
    def tile_position(self):
        return self.entity_rect