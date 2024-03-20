from astra.game.common.settings import WIDTH, HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT
from astra.objects.object import Object
from astra.objects.entities.properties.animation_manager import AnimationManager
from astra.objects.entities.properties.entity_properties import EntityProperties
from astra.objects.entities.sprite_managers.type.animated_sprite_manager import AnimatedSpriteManager
from astra.objects.indicators.type.attack_indicator import AttackIndicator
from astra.objects.indicators.type.move_indicator import MoveIndicator
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
            self.game.object_manager.remove_object(target)
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
        
    def is_within_range(self, value, min_max):
        return min_max[0] <= value <= min_max[1]

    def can_attack(self, entity, target_type):
        if isinstance(entity, target_type):
            return False
        dx, dy = abs(self.x - entity.x), abs(self.y - entity.y)
        return self.is_within_range(dx, self.properties.range) and self.is_within_range(dy, self.properties.range)
    
    def get_info(self):
        properties = self.properties 
        return (
            f"Name: {self.__class__.__name__}\n"
            f"Health: {properties.health}/{properties.max_health}\n"
            f"Damage: {properties.damage}\n"
            f"Range: {properties.range}\n"
            f"Speed: {properties.speed}\n"
            f"Inventory: {self.inventory.get_items()}"
        )
    
    def random_action(self):
        pass
    
    def apply_effect(self, effect):
        if effect.name == 'heal':
            self.heal(effect.value)
        elif effect.name == 'poison':
            self.poison(effect.value, effect.duration)
    
    def heal(self, amount):
        self.properties.health += amount
        self.properties.health = min(self.properties.health, self.properties.max_health)
        
    def poison(self, amount, duration):
        self.properties.health -= amount
        self.properties.health = max(self.properties.health, 0)
        self.properties.poisoned = duration
        self.properties.poison_amount = amount
        
    def check_status_effects(self):
        if self.properties.poisoned > 0:
            self.properties.health -= self.properties.poison_amount
            self.properties.poisoned -= 1
            
    def check_health(self):
        if self.properties.health <= 0:
            self.game.object_manager.remove_object(self)
            self.game.game_logic.check_game_over()