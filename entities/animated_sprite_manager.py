from game.settings import *
from .sprite_manager import SpriteManager
import pygame as pg

class AnimatedSpriteManager(SpriteManager):
    def __init__(self, entity):
        super().__init__(entity)
        self.idle_d = []
        self.idle_u = []
        self.attack_d = []
        self.attack_u = []
        self.load_sprite()

    def load_sprite(self):
        parent_class_name = self.entity.__class__.__bases__[0].__name__
        class_name = self.entity.__class__.__name__
        sprite_lists = ['idle_d', 'idle_u', 'attack_d', 'attack_u']
        for sprite_list in sprite_lists:
            getattr(self, sprite_list).extend(
                pg.image.load(f'images/{parent_class_name}/{class_name}/{sprite_list}{i}.png') for i in range(1, 3)
            )

    def get_sprite_based_on_state_and_orientation(self):
        if self.entity.state == "attacking":
            return self.get_attack_sprite()
        else:
            return self.get_idle_sprite()

    def get_attack_sprite(self):
        return self.attack_d[self.entity.animation_manager.current_frame] if self.entity.orientation == "down" else self.attack_u[self.entity.animation_manager.current_frame]

    def get_idle_sprite(self):
        return self.idle_d[self.entity.animation_manager.current_frame] if self.entity.orientation == "down" else self.idle_u[self.entity.animation_manager.current_frame]

    def flip_sprite_if_needed(self, sprite):
        return pg.transform.flip(sprite, True, False) if self.entity.flip else sprite

    def resize_sprite(self, sprite):
        return pg.transform.scale(sprite, (int(SPRITE_WIDTH * self.entity.game.camera.zoom), int(SPRITE_HEIGHT * self.entity.game.camera.zoom)))

    def blit_sprite(self, sprite):
        self.entity.game.screen.blit(sprite, (self.entity.x_iso - self.entity.game.camera.x, self.entity.y_iso - self.entity.game.camera.y))

    def create_mask_from_sprite(self, sprite):
        self.entity.entity_mask = pg.mask.from_surface(sprite)