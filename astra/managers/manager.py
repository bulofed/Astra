class Manager:
    def __init__(self):
        self.entities = []

    def add(self, entity):
        self.entities.append(entity)
        
    def add_multiple(self, entities):
        self.entities.extend(entities)

    def remove(self, entity):
        self.entities.remove(entity)

    def update(self):
        for entity in self.entities:
            entity.animation_manager.update()

    def draw(self):
        for entity in self.entities:
            entity.draw()