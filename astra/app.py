import pygame as pg
import sys
from astra.game.common.settings import RES, FPS
from astra.game.maps import Map
from astra.game.camera import Camera
from astra.game.game_logic import GameLogic
from astra.game.ui.menus.pause_menu import PauseMenu
from astra.managers.type.entity_manager import EntityManager
from astra.managers.type.item_manager import ItemManager
from astra.game.mouse_handler import MouseHandler
from astra.entities.items.item_entity import ItemEntity
from astra.entities.items.type.life_potion import LifePotion
from astra.entities.players.type.archer import Archer
from astra.entities.monsters.type.goblin import Goblin

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
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.mouse_handler.set_mouse()
        self.init_entities()
        pg.display.set_caption(self.map.name)

    def init_entities(self):
        self.entity_manager.add(Archer(self, 2, 2, 2))
        self.entity_manager.add(Goblin(self, 0, 2, 2))
        self.inventory_manager.add(ItemEntity(self, 2, 0, 2, LifePotion()))
        self.game_logic.current_entity = self.entity_manager.entities[0]

    def update(self):
        if not self.menus:
            self.entity_manager.update()
            self.inventory_manager.update(self.entity_manager.entities)
        pg.display.flip()
        self.delta = self.clock.tick(FPS)

    def draw(self):
        self.screen.fill('black')
        if not self.menus:
            self.map.draw(self.camera)
            self.entity_manager.draw()
            self.inventory_manager.draw()
            self.game_logic.current_entity.inventory.draw(self.screen)
        else:
            self.menus[-1].draw()
        self.mouse_handler.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
            elif (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and not self.menus):
                self.menus.append(PauseMenu(self))
            else:
                if self.menus:
                    self.menus[-1].handle_input(event)
                self.mouse_handler.handle_event(event)
                
    def pop_menu(self):
        self.menus.pop()

    def quit_game(self):
        pg.quit()
        sys.exit()

    def run(self):
        while True:
            game_over_message = self.game_logic.check_game_over()
            if game_over_message is not None:
                print(game_over_message)
                self.quit_game()
            self.mouse_handler.update()
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()
