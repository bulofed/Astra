from astra.game.ui.ui_component import UIComponent

class InfoPanel(UIComponent):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.entity = None

    def update(self, entity):
        self.entity = entity

    def draw(self):
        if self.entity is not None:
            info_text = str(self.entity.get_info())
            self.draw_text(info_text)