from managers.manager import Manager

class ItemManager(Manager):
    def __init__(self):
        super().__init__()
        
    def update(self, entities):
        for item in self.entities:
            item.update(self, entities)