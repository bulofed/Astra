import pygame as pg
from astra.game.ui.type.button import Button

class TextButton(Button):
    def __init__(self, text, x, y, width, height, color, bg_color, font, action=None, font_size=20):
        super().__init__(x, y, action)
        self.text = text
        self.width = width
        self.height = height
        self.color = color
        self.bg_color = bg_color
        self.font = font
        self.font_size = font_size

    def draw(self, win, outline=None):
        if outline:
            pg.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pg.draw.rect(win, self.bg_color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            text = self.font.render(self.text, 1, self.color)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
            
    def hover(self, pos):
        return (
            self.x < pos[0] < self.x + self.width
            and self.y < pos[1] < self.y + self.height
        )