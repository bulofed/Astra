from .uicomponent import *

class InfoPanel(UIComponent):
    def __init__(self, game, x, y, width, height):
        super().__init__(game, x, y, width, height)
        self.entity = None
        self.background = pg.Surface((width, height), pg.SRCALPHA)

    def update(self, entity):
        self.entity = entity

    def draw(self):
        if self.entity is not None:
            info_text = str(self.entity.get_info())
            text_surface = self.font.render(info_text, True, (255, 255, 255))
            self.game.screen.blit(text_surface, (self.rect.x, self.rect.y))
        else:
            self.game.screen.blit(self.background, self.rect)