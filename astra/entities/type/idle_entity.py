from astra.entities.entity import Entity
from astra.entities.sprite_managers.type.idle_sprite_manager import IdleSpriteManager
from astra.managers.sprite_manager_factory import SpriteManagerFactory

class IdleEntity(Entity):
    def __init__(self, game, x, y, z, properties=None):
        SpriteManagerFactory.register(IdleEntity, IdleSpriteManager)
        super().__init__(game, x, y, z, properties)
        
    def get_sprite_manager_type(self):
        return IdleEntity

    def draw(self):
        self.sprite_manager.draw()

    def update(self):
        self.sprite_manager.update()
        self.animation_manager.update()
        self.indicators_used[0].update()
        self.indicators_used[1].update()
        self.indicators_used[0].draw()
        self.indicators_used[1].draw()
        self.inventory.update()
        self.entity_mask = self.sprite_manager.get_entity_mask()
        self.entity_mask.x, self.entity_mask.y = self.x, self.y