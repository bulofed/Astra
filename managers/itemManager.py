class ItemManager():
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)
        
    def remove_item(self, item):
        self.items.remove(item)
        
    def update(self, entities):
        for item in self.items:
            item.update(self, entities)
        
    def draw(self):
        for item in self.items:
            item.draw()