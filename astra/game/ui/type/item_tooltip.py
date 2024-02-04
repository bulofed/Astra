from astra.game.ui.ui_component import UIComponent

class ItemTooltip(UIComponent):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.item = None

    def update(self, item):
        self.item = item

    def draw(self):
        if self.item is not None:
            item_name = self.item.name
            item_description = self.item.description
            text = f'{item_name}\n{item_description}'
            self.draw_text(text)