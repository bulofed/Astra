import pygame as pg
from game.settings import *

class Inventory:
    def __init__(self):
        self.items = {}
        box_image = pg.image.load('images/ui/inventory/Inventory_Slot_1.png')
        self.box_resized = pg.transform.scale(box_image, (INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT))
        self.box_rect = self.box_resized.get_rect()
        self.font = pg.font.SysFont(None, 32)

    def add_item(self, item):
        if len(self.items) >= MAX_ITEMS:
            return
        if item.name not in self.items:
            self.items[item.name] = (item, 1)
        else:
            item, count = self.items[item.name]
            self.items[item.name] = (item, count + 1)
            
    def use_item(self, item):
        if item.name in self.items:
            item, count = self.items[item.name]
            if count > 1:
                self.items[item.name] = (item, count - 1)
            else:
                self.remove_item(item)
            return True

    def remove_item(self, item):
        self.items.pop(item.name)

    def list_items(self):
        for item in self.items:
            print(f'Name: {item.name}, Description: {item.description}')
            
    def get_items(self):
        return ', '.join(f'{item.name} x{count}' for item, count in self.items.values())
    
    def draw(self, screen):
        """
        Draws the inventory on the screen.

        Args:
            screen: The surface to draw the inventory on.

        Returns:
            None
        """
        inventory_width = self.box_rect.width * MAX_ITEMS + (MAX_ITEMS - 1) * SPACE_BETWEEN_ITEMS
        start_x = (WIDTH - inventory_width) // 2
        
        for i in range(MAX_ITEMS):
            x = start_x + i * self.box_rect.width + i * SPACE_BETWEEN_ITEMS
            
            screen.blit(self.box_resized, (x, INVENTORY_Y))
            
            if i < len(self.items):
                item_name = list(self.items.keys())[i]
                item, count = self.items[item_name]
                item_resized = pg.transform.scale(item.sprite, (ITEM_SLOT_WIDTH, ITEM_SLOT_HEIGHT))
                item_x = x + (self.box_rect.width - item_resized.get_width()) // 2
                item_y = INVENTORY_Y + (self.box_rect.height - item_resized.get_height()) // 2
                screen.blit(item_resized, (item_x, item_y))
                text = self.font.render(f'x{count}', True, WHITE)
                count_x = x + self.box_rect.width - text.get_width() - ITEM_COUNT_OFFSET
                count_y = INVENTORY_Y + self.box_rect.height - text.get_height() - ITEM_COUNT_OFFSET
                screen.blit(text, (count_x, count_y))