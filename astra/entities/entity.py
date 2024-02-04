from astra.game.common.settings import WIDTH, HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT
from astra.entities.properties.animation_manager import AnimationManager
from astra.entities.properties.entity_properties import EntityProperties
from astra.managers.sprite_manager_factory import SpriteManagerFactory
from astra.indicators.type.attack_indicator import AttackIndicator
from astra.indicators.type.move_indicator import MoveIndicator
from astra.inventory.inventory import Inventory

class Entity():
    def __init__(self, game, x, y, z, properties=None):
        self.game = game
        self.x, self.y, self.z = x, y, z
        self.state = 'idle'
        self.orientation = 'down'
        self.flip = False
        self.sprite_manager = SpriteManagerFactory.create(self)
        self.animation_manager = AnimationManager(self)
        self.indicators_used = [AttackIndicator(game, self), MoveIndicator(game, self)]
        self.inventory = Inventory()
        self.properties = properties or EntityProperties()
        
    def get_sprite_manager_type(self):
        pass
        
    def update(self):
        self.animation_manager.update()
        
    def move(self, x, y, z):
        dx, dy = self.x - x, self.y - y
        self.set_orientation(dx, dy)
        self.x, self.y, self.z = x, y, z
        
    def attack(self, entity_manager, target):
        dx, dy = self.x - target.x, self.y - target.y
        self.set_orientation(dx, dy)
        self.animate_attack()
        target.properties.health -= self.properties.damage
        if target.properties.health <= 0:
            entity_manager.remove(target)
            self.game.game_logic.check_game_over()
            
    def set_orientation(self, dx, dy):
        if dx > 0 or dy > 0:
            self.orientation = 'up'
            self.flip = dy > 0
        elif dx < 0 or dy < 0:
            self.orientation = 'down'
            self.flip = dx < 0

            
    def animate_attack(self):
        self.state = 'attacking'
        self.animation_manager.current_frame = 0
            
    def is_clicked(self, mouse_handler):
        if hasattr(self, 'entity_mask'):
            overlap = self.entity_mask.overlap(
                mouse_handler.mouse_mask,
                (mouse_handler.mouse_x - self.sprite_manager.x_iso + self.game.camera.x,
                 mouse_handler.mouse_y - self.sprite_manager.y_iso + self.game.camera.y)
            )
            return overlap is not None
        else:
            return False
    
    def center_camera(self, camera):
        camera.x = self.sprite_manager.x_iso - WIDTH/2 + SPRITE_WIDTH/2 * camera.zoom
        camera.y = self.sprite_manager.y_iso - HEIGHT/2 + SPRITE_HEIGHT/2 * camera.zoom
        
    def can_attack(self, entity, target_type):
        if isinstance(entity, target_type):
            return False
        dx, dy = self.x - entity.x, self.y - entity.y
        return self.properties.range[0] <= abs(dx) <= self.properties.range[1] and self.properties.range[0] <= abs(dy) <= self.properties.range[1]
    
    def is_position_occupied(self, x, y, z):
        return any((x, y, z) in indicator.actions_positions for indicator in self.indicators_used)
    
    def get_info(self):
        return f"Name: {self.__class__.__name__}\nHealth: {self.properties.health}/{self.properties.max_health}\nDamage: {self.properties.damage}\nRange: {self.properties.range}\nSpeed: {self.properties.speed}\nInventory: {self.inventory.get_items()}"
    
    def random_action(self, _):
        pass
    
    def heal(self, amount):
        self.properties.health += amount
        self.properties.health = min(self.properties.health, self.properties.max_health)