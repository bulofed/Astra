from astra.managers.manager import Manager

class EntityManager(Manager):
    def draw(self):
        for entity in self.entities:
            entity.sprite_manager.draw()