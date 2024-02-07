from astra.game.common.settings import WIDTH, HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT
from astra.objects.object import Object
from astra.objects.entities.properties.animation_manager import AnimationManager
from astra.objects.entities.properties.entity_properties import EntityProperties
from astra.objects.entities.sprite_managers.type.animated_sprite_manager import AnimatedSpriteManager
from astra.indicators.type.attack_indicator import AttackIndicator
from astra.indicators.type.move_indicator import MoveIndicator
from astra.game.ui.inventory import Inventory

class Entity(Object):
    def __init__(self, game, x, y, z, properties=None):
        """An entity is a game object that can move and interact with other entities."""
        super().__init__(game, x, y, z)
        self.state = 'idle'
        self.orientation = 'down'
        self.flip = False
        self.sprite_manager = AnimatedSpriteManager(self.game, self)
        self.animation_manager = AnimationManager(self, game.delta)
        self.indicators_used = [AttackIndicator(self), MoveIndicator(self)]
        self.inventory = Inventory()
        self.properties = properties or EntityProperties()
        
    def draw(self, camera):
        self.sprite_manager.draw(camera)
    
    def update(self):
        self.animation_manager.update()
        
    def move(self, x, y, z):
        dx, dy = self.x - x, self.y - y
        self.set_orientation(dx, dy)
        self.x, self.y, self.z = x, y, z
        
    def attack(self, target):
        dx, dy = self.x - target.x, self.y - target.y
        self.set_orientation(dx, dy)
        self.animate_attack()
        target.properties.health -= self.properties.damage
        if target.properties.health <= 0:
            self.game.remove_object(target)
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
        return (self.properties.range[0] <= abs(dx) <= self.properties.range[1] and 0 <= abs(dy) <= self.properties.range[1]) or (self.properties.range[0] <= abs(dy) <= self.properties.range[1] and 0 <= abs(dx) <= self.properties.range[1])
    
    def is_position_occupied(self, x, y, z):
        return any((x, y, z) in indicator.actions_positions for indicator in self.indicators_used)
    
    def get_info(self):
        return f"Name: {self.__class__.__name__}\nHealth: {self.properties.health}/{self.properties.max_health}\nDamage: {self.properties.damage}\nRange: {self.properties.range}\nSpeed: {self.properties.speed}\nInventory: {self.inventory.get_items()}"
    
    def random_action(self, _):
        pass
    
    def heal(self, amount):
        self.properties.health += amount
        self.properties.health = min(self.properties.health, self.properties.max_health)