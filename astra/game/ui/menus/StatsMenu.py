from astra.game.ui.menus.menu import Menu
from astra.game.common.settings import WHITE
import pygame as py

class StatsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.display_stats()
        
    def display_stats(self):
        stats = self.game.game_logic.current_entity.stats
        font = py.font.Font(None, 30)
        text = font.render('Stats', True, WHITE)
        self.add_text(text, 10, 50)
        y = 100
        for key, value in stats.items():
            text = font.render(f'{key}: {value}', True, WHITE)
            self.add_text(text, 10, y)
            y += 30