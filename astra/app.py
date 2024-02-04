import pygame as pg
import sys
from astra.game.common.settings import RES, FPS
from astra.game.maps.map_generation import Map
from astra.game.camera import Camera
from astra.game.game_logic import GameLogic
from astra.game.ui.menus.select_player_menu import SelectPlayerMenu
from astra.game.ui.menus.pause_menu import PauseMenu
from astra.managers.type.entity_manager import EntityManager
from astra.managers.type.item_manager import ItemManager
from astra.game.mouse_handler import MouseHandler

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta = 1
        self.entity_manager = EntityManager()
        self.inventory_manager = ItemManager()
        self.game_logic = GameLogic(self.entity_manager)
        self.mouse_handler = MouseHandler(self)
        self.camera = Camera()
        self.menus = []
        self.level = 0
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.map.load_map(self.level)
        self.mouse_handler.set_mouse()
        self.menus.append(SelectPlayerMenu(self))
        pg.display.set_caption(self.map.name)
        
    def next_level(self):
        self.level += 1
        self.map.load_map(self.level)
        
    def update_game_state(self):
        self.entity_manager.update()
        self.inventory_manager.update(self.entity_manager.entities)

    def update(self):
        if not self.menus:
            self.update_game_state()
        pg.display.flip()
        self.delta = self.clock.tick(FPS)

    def draw_game_state(self):
        self.map.draw(self.camera)
        self.entity_manager.draw()
        self.inventory_manager.draw()
        self.game_logic.current_entity.inventory.draw(self.screen)

    def draw_menus(self):
        self.menus[-1].draw()

    def draw(self):
        self.screen.fill('black')
        if not self.menus:
            self.draw_game_state()
        else:
            self.draw_menus()
        self.mouse_handler.draw()

        
    def handle_input(self, event):
        if event.type == pg.QUIT:
            self.quit_game()
        elif (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and not self.menus):
            self.menus.append(PauseMenu(self))
        elif self.menus:
            self.menus[-1].handle_input(event)
        else:
            self.mouse_handler.handle_event(event)

    def check_events(self):
        for event in pg.event.get():
            self.handle_input(event)
                
    def pop_menu(self):
        self.menus.pop()

    def quit_game(self):
        pg.quit()
        sys.exit()

    def run(self):
        while True:
            game_over_message = self.game_logic.check_game_over()
            if game_over_message is not None and not self.menus:
                print(game_over_message)
                self.quit_game()
            self.mouse_handler.update()
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()
