from astra.game.common.settings import SPRITE_WIDTH, SPRITE_HEIGHT
from astra.game.common.utils import calculate_isometric_position
import pygame as pg

class AnimatedSpriteManager():
    def __init__(self, game, entity):
        self.idle_down = []
        self.idle_up = []
        self.attack_down = []
        self.attack_up = []
        self.game = game
        self.entity = entity
        self.load_sprite()

    def load_sprite(self):
        parent_class_name = self.entity.__class__.__bases__[0].__name__
        class_name = self.entity.__class__.__name__
        sprite_lists = ['idle_down', 'idle_up', 'attack_down', 'attack_up']
        for sprite_list in sprite_lists:
            getattr(self, sprite_list).extend(
                pg.image.load(f'astra/assets/images/{parent_class_name}/{class_name}/{sprite_list}{i}.png') for i in range(1, 3)
            )
            
    def draw(self, camera):
        self.x_iso, self.y_iso = calculate_isometric_position(self.entity.x, self.entity.y, self.entity.z, camera.zoom)
        
        screen_x = self.x_iso - camera.x
        screen_y = self.y_iso - camera.y
        
        offset_x = SPRITE_WIDTH * camera.zoom
        offset_y = SPRITE_HEIGHT * camera.zoom
        
        if -offset_x <= screen_x <= camera.width + offset_x and -offset_y <= screen_y <= camera.height + offset_y:
            sprite = self.get_sprite_based_on_state_and_orientation()
            sprite = self.flip_sprite_if_needed(sprite)
            sprite_resized = self.resize_sprite(sprite)
            self.blit_sprite(sprite_resized)
            self.create_mask_from_sprite(sprite_resized)

    def get_sprite_based_on_state_and_orientation(self):
        if self.entity.state == "attacking":
            return self.get_attack_sprite()
        else:
            return self.get_idle_sprite()

    def get_attack_sprite(self):
        return self.attack_down[self.entity.animation_manager.current_frame] if self.entity.orientation == "down" else self.attack_up[self.entity.animation_manager.current_frame]

    def get_idle_sprite(self):
        return self.idle_down[self.entity.animation_manager.current_frame] if self.entity.orientation == "down" else self.idle_up[self.entity.animation_manager.current_frame]

    def flip_sprite_if_needed(self, sprite):
        return pg.transform.flip(sprite, True, False) if self.entity.flip else sprite

    def resize_sprite(self, sprite):
        return pg.transform.scale(sprite, (int(SPRITE_WIDTH * self.entity.game.camera.zoom), int(SPRITE_HEIGHT * self.entity.game.camera.zoom)))

    def blit_sprite(self, sprite):
        self.entity.game.screen.blit(sprite, (self.x_iso - self.entity.game.camera.x, self.y_iso - self.entity.game.camera.y))

    def create_mask_from_sprite(self, sprite):
        self.entity.entity_mask = pg.mask.from_surface(sprite)