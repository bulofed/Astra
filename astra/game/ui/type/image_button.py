import pygame as pg
from astra.game.ui.type.button import Button

class ImageButton(Button):
    def __init__(self, x, y, image, action=None):
        super().__init__(x, y, action)
        self.image = image

    def draw(self, win, outline=None):
        if outline:
            pg.draw.rect(win, outline, (self.x-2, self.y-2, self.image.get_width()+4, self.image.get_height()+4), 0)

        win.blit(self.image, (self.x, self.y))
        
    def hover(self, pos):
        return self.x < pos[0] < self.x + self.image.get_width() and self.y < pos[1] < self.y + self.image.get_height()