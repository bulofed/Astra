class Manager:
    def __init__(self):
        self.entities = []

    def add(self, entity):
        self.entities.append(entity)

    def remove(self, entity):
        self.entities.remove(entity)

    def update(self):
        for entity in self.entities:
            entity.update()

    def draw(self):
        for entity in self.entities:
            entity.draw()