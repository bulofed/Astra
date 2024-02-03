from astra.managers.manager import Manager

class ItemManager(Manager):
    def update(self, entities):
        for item in self.entities:
            item.update(self, entities)