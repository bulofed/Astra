from game.settings import *
from indicators.type.attackIndicator import  *
from indicators.type.moveIndicator import *
from inventory.inventory import *
import pygame as pg

class Entity():
    def __init__(self, game, x, y, z):
        self.game = game
        self.x, self.y, self.z = x, y, z
        self.state = 'idle'
        self.orientation = 'down'
        self.flip = False
        self.current_frame = 0
        self.animation_time = 0
        self.frame_duration = .5
        self.idle_d = []
        self.idle_u = []
        self.attack_d = []
        self.attack_u = []
        self.load_sprites()
        self.indicators_used = [AttackIndicator(game, self), MoveIndicator(game, self)]
        self.inventory = Inventory()
        self.speed = 1 # Default speed
        self.range = 1 # Default range
        self.max_health = 20 # Default max health
        self.health = self.max_health
        self.damage = 5 # Default damage
    
    def load_sprites(self):
        parent_class_name = self.__class__.__bases__[0].__name__
        class_name = self.__class__.__name__
        sprite_lists = ['idle_d', 'idle_u', 'attack_d', 'attack_u']
        for sprite_list in sprite_lists:
            getattr(self, sprite_list).extend(
                pg.image.load(f'images/{parent_class_name}/{class_name}/{sprite_list}{i}.png') for i in range(1, 3)
            )
        
    def update(self):
        self.animation_time += self.game.delta / 1000
        if self.animation_time >= self.frame_duration:
            self.animation_time -= self.frame_duration
            if self.state == "attacking":
                self.current_frame = (
                    (self.current_frame + 1) % len(self.attack_d)
                    if self.orientation == "down"
                    else (self.current_frame + 1) % len(self.attack_u)
                )
                if self.current_frame == 0:
                    self.state = "idle"
            elif self.orientation == "down":
                self.current_frame = (self.current_frame + 1) % len(self.idle_d)
            else:
                self.current_frame = (self.current_frame + 1) % len(self.idle_u)

    def draw(self):
        self.x_iso, self.y_iso = self.game.map.calculate_isometric_position(self.x, self.y, self.z, self.game.camera.zoom)
        if self.state == "attacking":
            sprite = (
                self.attack_d[self.current_frame]
                if self.orientation == "down"
                else self.attack_u[self.current_frame]
            )
        elif self.orientation == "down":
            sprite = self.idle_d[self.current_frame]
        else:
            sprite = self.idle_u[self.current_frame]
        if self.flip:
            sprite = pg.transform.flip(sprite, True, False)
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
        dx, dy = x - self.x, y - self.y
        self.set_orientation(dx, dy)
        self.x, self.y, self.z = x, y, z
        
    def attack(self, target):
        dx, dy = target.x - self.x, target.y - self.y
        self.set_orientation(dx, dy)
        self.animate_attack()
        target.health -= self.damage
        if target.health <= 0:
            self.game.entities.remove(target)
            self.game.check_game_over()
            
    def set_orientation(self, dx, dy):
        if dy > 0:
            self.orientation = 'down'
            self.flip = False
        elif dy < 0:
            self.orientation = 'up'
            self.flip = True
        elif dx < 0:
            self.orientation = 'up'
            self.flip = False
        elif dx > 0:
            self.orientation = 'down'
            self.flip = True
            
    def animate_attack(self):
        self.state = 'attacking'
        self.current_frame = 0
            
    def is_clicked(self, mouse_pos):
        if hasattr(self, 'entity_mask'):
            return self.entity_mask.overlap(self.game.mouse_mask, (mouse_pos[0] - self.x_iso + self.game.camera.x, mouse_pos[1] - self.y_iso + self.game.camera.y)) != None
        else:
            return False
    
    def center_camera(self, camera):
        camera.x = self.x_iso - WIDTH/2 + SPRITE_WIDTH/2 * camera.zoom
        camera.y = self.y_iso - HEIGHT/2 + SPRITE_HEIGHT/2 * camera.zoom
        
    def can_attack(self, entity, target_type):
        if isinstance(entity, target_type):
            return False
        dx, dy, dz = entity.x - self.x, entity.y - self.y, entity.z - self.z
        return abs(dx) <= self.range and abs(dy) <= self.range and abs(dz) <= self.range and (dx != 0 or dy != 0 or dz != 0)
    
    def is_position_occupied(self, x, y, z):
        """
        Checks if the specified position is occupied.

        Args:
            self: The player instance.
            x: The x-coordinate of the position to check.
            y: The y-coordinate of the position to check.
            z: The z-coordinate of the position to check.

        Returns:
            True if the position is occupied, False otherwise.
        """
        return any((x, y, z) in indicator.actions_positions for indicator in self.indicators_used)
    
    def get_info(self):
        return f"Name: {self.__class__.__name__}\nHealth: {self.health}/{self.max_health}\nDamage: {self.damage}\nRange: {self.range}\nSpeed: {self.speed}\nInventory: {self.inventory.get_items()}"