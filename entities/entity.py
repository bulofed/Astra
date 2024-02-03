from game.settings import *
from game.utils import calculate_isometric_position
from managers.animationManager import *
from .animated_sprite_manager import AnimatedSpriteManager
from .idle_sprite_manager import ItemSpriteManager
from indicators.type.attackIndicator import  *
from indicators.type.moveIndicator import *
from inventory.inventory import *

class Entity():
    def __init__(self, game, x, y, z, is_item=False):
        self.game = game
        self.x, self.y, self.z = x, y, z
        self.state = 'idle'
        self.orientation = 'down'
        self.flip = False
        if is_item:
            self.sprite_manager = ItemSpriteManager(self)
        else:
            self.sprite_manager = AnimatedSpriteManager(self)
        self.animation_manager = AnimationManager(self)
        self.indicators_used = [AttackIndicator(game, self), MoveIndicator(game, self)]
        self.inventory = Inventory()
        self.speed = 1 # Default speed
        self.range = 1 # Default range
        self.max_health = 20 # Default max health
        self.health = self.max_health
        self.damage = 5 # Default damage
        
    def update(self):
        self.animation_manager.update()

    def draw(self):
        self.x_iso, self.y_iso = calculate_isometric_position(self.x, self.y, self.z, self.game.camera.zoom)
        sprite = self.sprite_manager.get_sprite_based_on_state_and_orientation()
        sprite = self.sprite_manager.flip_sprite_if_needed(sprite)
        sprite_resized = self.sprite_manager.resize_sprite(sprite)
        self.sprite_manager.blit_sprite(sprite_resized)
        self.sprite_manager.create_mask_from_sprite(sprite_resized)
        
    def move(self, x, y, z):
        dx, dy = x - self.x, y - self.y
        self.set_orientation(dx, dy)
        self.x, self.y, self.z = x, y, z
        
    def attack(self, entity_manager, target):
        dx, dy = target.x - self.x, target.y - self.y
        self.set_orientation(dx, dy)
        self.animate_attack()
        target.health -= self.damage
        if target.health <= 0:
            entity_manager.remove(target)
            self.game.game_logic.check_game_over()
            
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
        self.animation_manager.current_frame = 0
            
    def is_clicked(self, mouse_handler):
        if hasattr(self, 'entity_mask'):
            return self.entity_mask.overlap(mouse_handler.mouse_mask, (mouse_handler.mouse_x - self.x_iso + self.game.camera.x, mouse_handler.mouse_y - self.y_iso + self.game.camera.y)) != None
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
        return any((x, y, z) in indicator.actions_positions for indicator in self.indicators_used)
    
    def get_info(self):
        return f"Name: {self.__class__.__name__}\nHealth: {self.health}/{self.max_health}\nDamage: {self.damage}\nRange: {self.range}\nSpeed: {self.speed}\nInventory: {self.inventory.get_items()}"
    
    def random_action(self, _):
        pass