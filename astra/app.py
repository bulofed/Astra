import pygame as pg
import sys
from astra.game.common.settings import RES, FPS
from astra.game.maps.map_generation import Map
from astra.game.camera import Camera
from astra.game.object_manager import ObjectManager
from astra.game.game_logic import GameLogic
from astra.game.ui.menus.select_player_menu import SelectPlayerMenu
from astra.game.ui.menus.pause_menu import PauseMenu
from astra.game.mouse_handler import MouseHandler

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta = 1
        self.game_logic = GameLogic()
        self.object_manager = ObjectManager(self)
        self.mouse_handler = MouseHandler(self)
        self.camera = Camera(RES[0], RES[1])
        self.menus = []
        self.level = 0
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.mouse_handler.set_mouse()
        self.menus.append(SelectPlayerMenu(self))
        
    def start_game(self, level):
        self.map.load_map(level)
        self.mouse_handler.set_mouse()
        self.menus.clear()
        pg.display.set_caption(self.map.name)
        
    def next_level(self):
        self.level += 1
        self.map.load_map(self.level)

    def update(self):
        if not self.menus:
            self.object_manager.update()
        pg.display.flip()
        self.delta = self.clock.tick(FPS)

    def draw(self):
        self.screen.fill('black')
        if not self.menus:
            self.object_manager.draw()
            self.game_logic.current_entity.inventory.draw(self.screen)
        else:
            self.menus[-1].draw()
        self.mouse_handler.draw()

        
    def handle_input(self, event):
        if event.type == pg.QUIT:
            self.quit_game()
        elif (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and not self.menus):
            self.push_menu(PauseMenu(self))
        elif self.menus:
            self.menus[-1].handle_input(event)
        else:
            self.mouse_handler.handle_event(event)
            
    def push_menu(self, menu):
        self.menus.append(menu)

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
