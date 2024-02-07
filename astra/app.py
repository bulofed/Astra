import pygame as pg
import sys
from astra.game.common.settings import RES, FPS
from astra.game.maps.map_generation import Map
from astra.game.camera import Camera
from astra.game.game_logic import GameLogic
from astra.game.ui.menus.select_player_menu import SelectPlayerMenu
from astra.game.ui.menus.pause_menu import PauseMenu
from astra.game.mouse_handler import MouseHandler
from astra.objects.entities.entity import Entity
from astra.indicators.indicator import Indicator

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta = 1
        self.objects = []
        self.game_logic = GameLogic()
        self.mouse_handler = MouseHandler(self)
        self.camera = Camera()
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
        entities = [obj for obj in self.objects if isinstance(obj, Entity)]
        self.game_logic.set_entities(entities)
        pg.display.set_caption(self.map.name)
        
    def add_object(self, obj):
        self.objects.append(obj)
        
    def remove_object(self, obj):
        self.objects.remove(obj)
        
    def clear_objects(self):
        self.objects.clear()
        
    def get_object(self, x, y, z, type=None):
        return next(
            (
                obj
                for obj in self.objects
                if obj.x == x and obj.y == y and obj.z == z and isinstance(obj, type)
            ),
            None,
        )
        
    def get_entity(self, x, y, z):
        return self.get_object(x, y, z, Entity)
        
    def get_objects(self, type=None):
        return [obj for obj in self.objects if isinstance(obj, type)]
        
    def draw_objects(self):
        objects = sorted(self.objects, key=lambda obj: (obj.z, isinstance(obj, Entity), isinstance(obj, Indicator), obj.y, obj.x))
        print(objects)
        for obj in objects:
            obj.draw(self.camera)
        
    def next_level(self):
        self.level += 1
        self.map.load_map(self.level)
        
    def update_objects(self):
        for obj in self.objects:
            obj.update()

    def update(self):
        if not self.menus:
            self.update_objects()
        pg.display.flip()
        self.delta = self.clock.tick(FPS)

    def draw(self):
        self.screen.fill('black')
        if not self.menus:
            self.draw_objects()
        else:
            self.menus[-1].draw()
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
