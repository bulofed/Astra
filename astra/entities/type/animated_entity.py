from astra.entities.entity import Entity
from astra.entities.sprite_managers.type.animated_sprite_manager import AnimatedSpriteManager
from astra.managers.sprite_manager_factory import SpriteManagerFactory

class AnimatedEntity(Entity):
    def __init__(self, game, x, y, z, properties=None):
        SpriteManagerFactory.register(AnimatedEntity, AnimatedSpriteManager)
        super().__init__(game, x, y, z, properties)
        
    def get_sprite_manager_type(self):
        return AnimatedEntity

    def draw(self):
        self.sprite_manager.draw()

    def update(self):
        self.animation_manager.update()