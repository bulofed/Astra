import pygame as pg
from astra.game.common.settings import WIDTH, WHITE, INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT, MAX_ITEMS, SPACE_BETWEEN_ITEMS, INVENTORY_Y, ITEM_SLOT_WIDTH, ITEM_SLOT_HEIGHT

class Inventory:
    def __init__(self):
        self.items = {}
        box_image = pg.image.load('astra/assets/ui/inventory/inventory_slot_1.png')
        self.box_resized = pg.transform.scale(box_image, (INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT))
        self.box_rect = self.box_resized.get_rect()
        self.font = pg.font.SysFont(None, 32)
        total_width = self.box_rect.width * MAX_ITEMS
        total_spacing = (MAX_ITEMS - 1) * SPACE_BETWEEN_ITEMS
        self.initial_offset = (WIDTH - total_width - total_spacing) // 2

    def _calculate_position(self, index, item_resized=None):
        item_offset = index * (self.box_rect.width + SPACE_BETWEEN_ITEMS)

        x = self.initial_offset + item_offset
        y = INVENTORY_Y

        if item_resized:
            item_width_offset = (self.box_rect.width - item_resized.get_width()) // 2
            item_height_offset = (self.box_rect.height - item_resized.get_height()) // 2

            x += item_width_offset
            y += item_height_offset

        return x, y

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
        return (f'Name: {item.name}, Description: {item.description}' for item in self.items.values())

    def get_items(self):
        return ', '.join([f'{item.name} x{count}' for item, count in self.items.values()])

    def get_item_at(self, pos):
        for i, item_name in enumerate(self.items.keys()):
            x, y = self._calculate_position(i)
            rect = pg.Rect(x, y, self.box_rect.width, self.box_rect.height)
            if rect.collidepoint(pos):
                return self.items[item_name][0]
        return None

    def draw(self, screen):
        pre_scaled_sprites = self._pre_scale_sprites()
        pre_rendered_counts = self._pre_render_counts()

        for i in range(MAX_ITEMS):
            x, y = self._calculate_position(i)
            screen.blit(self.box_resized, (x, y))

            if i < len(self.items):
                item_name = list(self.items.keys())[i]
                _, count = self.items[item_name]
                self._draw_item(screen, item_name, count, i, pre_scaled_sprites, pre_rendered_counts)

    def _pre_scale_sprites(self):
        return {
            item_name: pg.transform.scale(item.sprite, (ITEM_SLOT_WIDTH, ITEM_SLOT_HEIGHT))
            for item_name, (item, _) in self.items.items()
        }

    def _pre_render_counts(self):
        return {
            count: self.font.render(f'x{count}', True, WHITE)
            for _, count in self.items.values()
        }

    def _draw_item(self, screen, item_name, count, i, pre_scaled_sprites, pre_rendered_counts):
        item_resized = pre_scaled_sprites[item_name]
        item_x, item_y = self._calculate_position(i, item_resized)
        screen.blit(item_resized, (item_x, item_y))
        text = pre_rendered_counts[count]
        count_x, count_y = self._calculate_count_position(i, text)
        screen.blit(text, (count_x, count_y))

    def _calculate_count_position(self, i, text):
        item_offset = i * (self.box_rect.width + SPACE_BETWEEN_ITEMS)
        text_offset = self.box_rect.width - text.get_width() - 10

        count_x = self.initial_offset + item_offset + text_offset
        count_y = INVENTORY_Y + self.box_rect.height - text.get_height() - 10
        return count_x, count_y