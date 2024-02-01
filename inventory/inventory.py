class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def list_items(self):
        for item in self.items:
            print(f'Name: {item.name}, Description: {item.description}')
            
    def get_items(self):
        return ', '.join(f'{item.name}' for item in self.items)