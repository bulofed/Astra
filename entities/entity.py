from abc import ABC, abstractmethod
from game.settings import *
from indicators.type.attackIndicator import  *
from indicators.type.moveIndicator import *
import pygame as pg

class Entity(ABC):
    def __init__(self, game, x, y, z):
        self.game = game
        self.x, self.y, self.z = x, y, z
        self.current_frame = 0
        self.animation_time = 0
        self.frame_duration = .5
        self.load_sprites()
        self.indicators_used= [AttackIndicator(game, self), MoveIndicator(game, self)]
    
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
        
    def move(self, x, y, z):
        """
        Moves the entity to the specified position.

        Args:
            self: The entity instance.
            x: The x-coordinate of the position to move to.
            y: The y-coordinate of the position to move to.
            z: The z-coordinate of the position to move to.

        Returns:
            None
        """
        self.x, self.y, self.z = x, y, z
        
    def attack(self, target):
        target.health -= self.damage
        if target.health <= 0:
            self.game.entities.remove(target)
            self.game.check_game_over()
            
    def is_clicked(self, mouse_pos):
        return self.entity_mask.overlap(self.game.mouse_mask, (mouse_pos[0] - self.x_iso + self.game.camera.x, mouse_pos[1] - self.y_iso + self.game.camera.y)) != None
    
    def center_camera(self, camera):
        camera.x = self.x_iso - WIDTH/2 + SPRITE_WIDTH/2 * camera.zoom
        camera.y = self.y_iso - HEIGHT/2 + SPRITE_HEIGHT/2 * camera.zoom
        
    def can_attack(self, entity, target_type):
        if isinstance(entity, target_type):
            return False
        dx, dy, dz = entity.x - self.x, entity.y - self.y, entity.z - self.z
        return abs(dx) <= self.range and abs(dy) <= self.range and abs(dz) <= self.range and (dx != 0 or dy != 0 or dz != 0)