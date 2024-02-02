from game.uicomponent import UIComponent

class ItemTooltip(UIComponent):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 200, 100)  # Adjust width and height as needed
        self.item = None

    def update(self, item):
        self.item = item

    def draw(self):
        if self.item is not None:
            item_name = self.item.name
            item_description = self.item.description
            text = f'{item_name}\n{item_description}'
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.game.screen.blit(text_surface, (self.rect.x, self.rect.y))