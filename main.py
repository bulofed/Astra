import pygame as pg
import sys
from game.settings import *
from game.maps import *
from game.camera import *
from game.infopanel import *
from game.itemtooltip import *
from managers.entityManager import *
from entities.items.itemEntity import *
from inventory.items.lifePotion import *
from entities.players.type.swordman import *
from entities.monsters.type.goblin import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta = 1
        self.items = []
        self.entity_manager = EntityManager()
        self.new_game()
        self.camera = Camera()
        self.info_panel = InfoPanel(self, 20, 20, WIDTH, HEIGHT)
        self.item_tooltip = ItemTooltip(self, 20, HEIGHT - INVENTORY_Y_OFFSET - FONT_SIZE*2)
        self.dragging = False
        self.selected_player = None
        self.selected_entity = None

    def new_game(self):
        """
        Starts a new game by initializing the map and player.

        Args:
            None

        Returns:
            None
        """
        self.map = Map(self)
        self.mouse = pg.Surface((5, 5))
        self.set_mouse()
        self.init_entities()
        self.entity_manager.current_entity = self.entity_manager.entities[self.entity_manager.current_turn]

    def set_mouse(self):
        pg.mouse.set_visible(False)
        self.mouse.fill('red')
        self.mouse_mask = pg.mask.from_surface(self.mouse)

    def init_entities(self):
        self.entity_manager.add_entity(Swordman(self, 2, 2, 2))
        self.entity_manager.add_entity(Goblin(self, 0, 2, 2))
        self.items.append(ItemEntity(self, 2, 0, 2, LifePotion()))

    def update(self):
        """
        Updates the game state.

        Args:
            None

        Returns:
            None
        """
        self.entity_manager.update_entities()
        for item in self.items:
            item.update(self.entity_manager.entities)
        pg.display.flip()
        self.delta = self.clock.tick(FPS)
        pg.display.set_caption(self.map.name)
        self.info_panel.update(self.selected_entity)

    def draw(self):
        """
        Draws the game on the screen.

        Args:
            None

        Returns:
            None
        """
        self.screen.fill('black')
        self.map.draw(self.camera)
        self.entity_manager.draw_entities()
        for item in self.items:
            item.draw()
        self.entity_manager.current_entity.inventory.draw(self.screen)
        self.screen.blit(self.mouse, self.mouse_pos)
        self.info_panel.draw()
        self.item_tooltip.draw()

    def check_events(self):
        """
        Checks for and handles game events.

        Args:
            None

        Returns:
            None
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.quit_game()
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.handle_mouse_button_down(event)
            elif event.type == pg.MOUSEBUTTONUP:
                self.handle_mouse_button_up(event)
            elif event.type == pg.MOUSEMOTION:
                self.handle_mouse_motion()

    def quit_game(self):
        """
        Quits the game.

        Args:
            None

        Returns:
            None
        """
        pg.quit()
        sys.exit()

    def handle_mouse_button_down(self, event):
        """
        Handles mouse button down events.

        Args:
            event: The mouse button down event.

        Returns:
            None
        """
        if event.button == 1:
            self.handle_left_click()
            self.dragging = True
            self.drag_start = self.mouse_pos
        elif event.button in [4, 5]:
            self.adjust_zoom(event.button)

    def handle_left_click(self):
        clicked_entity = self.get_clicked_entity(self.mouse_pos)
        
        if self.hovered_item is not None:
            self.hovered_item.use(self.entity_manager.current_entity)

        if self.selected_player is None and self.is_player_turn(clicked_entity):
            self.select_player(clicked_entity)
        elif self.selected_player is not None:
            if not self.selected_player.handle_click(self.entity_manager, self.mouse_pos, self.camera):
                self.selected_player = None

    def get_clicked_entity(self, mouse_pos):
        return next(
            (entity for entity in self.entity_manager.entities if entity.is_clicked(mouse_pos)),
            None,
        )

    def get_item_entity_at(self, x, y, z):
        return next(
            (entity for entity in self.entity_manager.entities if isinstance(entity, ItemEntity)
             and entity.x == x and entity.y == y and entity.z == z),
            None,
        )

    def is_player_turn(self, entity):
        return isinstance(entity, Player) and entity == self.entity_manager.current_entity

    def select_player(self, player):
        self.selected_player = player
        player.show_actions(self.entity_manager.entities)

    def adjust_zoom(self, button):
        """
        Adjusts the zoom level of the camera.

        Args:
            button: The mouse button that was clicked.

        Returns:
            None
        """
        zoom_adjustment = .5 if button == 4 else -.5
        self.camera.set_zoom(self.camera.zoom + zoom_adjustment)

    def handle_mouse_button_up(self, event):
        """
        Handles mouse button up events.

        Args:
            event: The mouse button up event.

        Returns:
            None
        """
        if event.button == 1:
            self.dragging = False

    def handle_mouse_motion(self):
        """
        Handles mouse motion events.

        Args:
            None

        Returns:
            None
        """
        hovered_entity = self.get_clicked_entity(self.mouse_pos)
        self.selected_entity = hovered_entity if hovered_entity is not None else None
        
        self.hovered_item = self.entity_manager.current_entity.inventory.get_item_at(self.mouse_pos)
        if self.hovered_item is not None:
            self.item_tooltip.update(self.hovered_item)
        else:
            self.item_tooltip.update(None)
        
        if self.dragging:
            dx, dy = self.mouse_x - self.drag_start[0], self.mouse_y - self.drag_start[1]
            self.camera.move(-dx, -dy)
            self.drag_start = (self.mouse_x, self.mouse_y)

    def check_game_over(self):
        """
        Checks if the game is over.

        Args:
            None

        Returns:
            None
        """
        players = [
            entity for entity in self.entity_manager.entities if isinstance(entity, Player)]
        monsters = [
            entity for entity in self.entity_manager.entities if isinstance(entity, Monster)]

        if not players:
            print("Game Over: All players have been eliminated.")
            self.quit_game()
        elif not monsters:
            print("Victory: All monsters have been eliminated.")
            self.quit_game()

    def run(self):
        """
        Runs the game loop.

        Args:
            None

        Returns:
            None
        """
        while True:
            self.mouse_pos = self.mouse_x, self.mouse_y = pg.mouse.get_pos()
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
