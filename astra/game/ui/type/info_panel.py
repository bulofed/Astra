from astra.game.ui.ui_component import UIComponent

class InfoPanel(UIComponent):
    def __init__(self, game, x, y, width, height):
        super().__init__(game, x, y, width, height)
        self.entity = None

    def update(self, entity):
        self.entity = entity

    def draw(self):
        if self.entity is not None:
            info_text = str(self.entity.get_info())
            text_surface = self.font.render(info_text, True, (255, 255, 255))
            self.game.screen.blit(text_surface, (self.rect.x, self.rect.y))