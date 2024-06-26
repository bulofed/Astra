from astra.game.ui.menus.menu import Menu
from astra.game.ui.type.text_button import TextButton
from astra.game.common.settings import WIDTH, HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, WHITE, GREY
from astra.game.ui.menus.StatsMenu import StatsMenu
import pygame as py

class PauseMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.init_buttons()
    
    def init_buttons(self):
        buttons_x = WIDTH // 2 - BUTTON_WIDTH // 2
        resume_y = HEIGHT // 2 - BUTTON_HEIGHT // 3 * 2
        stats_y = resume_y + BUTTON_HEIGHT + 10
        quit_y = stats_y + BUTTON_HEIGHT + 10
        bg_color = GREY
        color = WHITE
        font = py.font.SysFont("notosans", 20)
        resume_button = TextButton("Resume", buttons_x, resume_y, BUTTON_WIDTH, BUTTON_HEIGHT, color, bg_color, font, self.resume)
        stats_button = TextButton("Stats", buttons_x, stats_y, BUTTON_WIDTH, BUTTON_HEIGHT, color, bg_color, font, self.stats)
        quit_button = TextButton("Quit", buttons_x, quit_y, BUTTON_WIDTH, BUTTON_HEIGHT, color, bg_color, font, self.quit)
        self.add_button(resume_button)
        self.add_button(stats_button)
        self.add_button(quit_button)

    def resume(self):
        self.game.pop_menu()
        
    def stats(self):
        self.game.push_menu(StatsMenu(self.game))

    def quit(self):
        self.game.quit_game()