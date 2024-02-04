from astra.game.ui.menus.menu import Menu
from astra.game.ui.type.button import Button
from astra.game.common.settings import WIDTH, HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, WHITE, GREY
import pygame as py

class PauseMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.init_buttons()
    
    def init_buttons(self):
        resume_x = WIDTH // 2 - BUTTON_WIDTH // 2
        resume_y = HEIGHT // 2 - BUTTON_HEIGHT // 2
        bg_color = GREY
        color = WHITE
        font = py.font.SysFont("notosans", 20)
        resume_button = Button("Resume", resume_x, resume_y, BUTTON_WIDTH, BUTTON_HEIGHT, color, bg_color, font, self.resume)
        quit_button = Button("Quit", resume_x, resume_y + BUTTON_HEIGHT + 10, BUTTON_WIDTH, BUTTON_HEIGHT, color, bg_color, font, self.quit)
        self.add_button(resume_button)
        self.add_button(quit_button)

    def resume(self):
        self.game.pop_menu()

    def quit(self):
        self.game.quit_game()