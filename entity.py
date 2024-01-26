from abc import ABC, abstractmethod
from settings import *
import pygame as pg

class Entity(ABC):
    def __init__(self, game, x, y, z):
        self.game = game
        self.x, self.y, self.z = x, y, z
        self.current_frame = 0
        self.animation_time = 0
        self.frame_duration = .5
        self.speed = 1
        self.load_sprites()
    
    @abstractmethod
    def load_sprites(self):
        pass
        
    def update(self):
        self.animation_time += self.game.delta / 1000
        if self.animation_time >= self.frame_duration:
            self.animation_time -= self.frame_duration
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self):
        self.x_iso, self.y_iso = self.game.map.calculate_isometric_position(self.x, self.y, self.z, self.game.camera.zoom)
        sprite = self.sprites[self.current_frame]
        sprite_resized = pg.transform.scale(sprite, (int(SPRITE_WIDTH * self.game.camera.zoom), int(SPRITE_HEIGHT * self.game.camera.zoom)))
        self.game.screen.blit(sprite_resized, (self.x_iso - self.game.camera.x, self.y_iso - self.game.camera.y))
        self.entity_mask = pg.mask.from_surface(sprite_resized)
        
    def attack(self, target):
        target.health -= self.damage
        if target.health <= 0:
            self.game.entities.remove(target)