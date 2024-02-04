from astra.game.ui.menus.menu import Menu
from astra.game.ui.type.image_button import ImageButton
from astra.game.common.settings import WIDTH, HEIGHT
import pygame as py

class SelectPlayerMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.init_images()
        
    def _load_icon(self, image_path):
        return py.image.load(image_path)

    def _copy_background(self, bg):
        return bg.copy()

    def _blit_icon(self, icon_image, icon, bg_rect):
        icon_image.blit(icon, (bg_rect.width // 4, bg_rect.height // 4))
        return icon_image

    def _calculate_button_x(self, icon_image, index):
        return (WIDTH // (self.total + 1)) * (index + 1) - icon_image.get_width() // 2

    def _create_icon(self, image_path, index, action, bg):
        icon = self._load_icon(image_path)
        icon_image = self._copy_background(bg)
        icon_image = self._blit_icon(icon_image, icon, bg.get_rect())
        button_x = self._calculate_button_x(icon_image, index)
        button_y = HEIGHT // 2 - icon_image.get_height() // 2
        return ImageButton(button_x, button_y, icon_image, action)
    
    def _blit_icon(self, icon_image, icon, bg_rect):
        icon_image.blit(icon, (bg_rect.width // 4, bg_rect.height // 4))
        return py.transform.scale(icon_image, (100, 100))
    
    def _calculate_button_x(self, icon_image, index):
        spacing = WIDTH // (len(self.icons) + 1)
        center_offset = icon_image.get_width() // 2
        return spacing * (index + 1) - center_offset

    def init_images(self):
        bg = py.image.load("astra/assets/ui/menu/player_bg.png")

        self.icons = [
            ("astra/assets/ui/menu/swordman_icon.png", self.select_swordman),
            ("astra/assets/ui/menu/archer_icon.png", self.select_archer)
        ]
        for i, (icon_path, action) in enumerate(self.icons):
            button = self._create_icon(icon_path, i, action, bg)
            self.add_button(button)
        
    def select_swordman(self):
        self.game.pop_menu()
        self.game.init_entities("swordman")
        
    def select_archer(self):
        self.game.pop_menu()
        self.game.init_entities("archer")