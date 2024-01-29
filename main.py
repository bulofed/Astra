import pygame as pg
import sys
from game.settings import *
from game.maps import *
from game.camera import *
from entities.player.player import *
from entities.monsters.type.goblin import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta = 1
        self.entities = []
        self.current_turn = 0
        self.new_game()
        self.camera = Camera()
        self.dragging = False
        self.selected_player = None
     
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
    
    def set_mouse(self):
        pg.mouse.set_visible(False)
        self.mouse.fill('red')
        self.mouse_mask = pg.mask.from_surface(self.mouse)
    
    def init_entities(self):
        self.entities.append(Player(self, 2, 2, 2))
        self.entities.append(Goblin(self, 0, 2, 2))
    
    def update(self):
        """
        Updates the game state.

        Args:
            None

        Returns:
            None
        """
        for entity in self.entities:
            entity.update()
        pg.display.flip()
        self.delta =  self.clock.tick(FPS)
        pg.display.set_caption(self.map.name)
        
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
        for entity in self.entities:
            entity.draw()
        self.screen.blit(self.mouse, self.mouse_pos)
        
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
            self.drag_start = pg.mouse.get_pos()
        elif event.button in [4, 5]:
            self.adjust_zoom(event.button)

    def handle_left_click(self):
        x, y = pg.mouse.get_pos()
        clicked_entity = self.get_clicked_entity((x, y))

        if self.selected_player is None and self.is_player_turn(clicked_entity):
            self.select_player(clicked_entity)
        elif self.selected_player is not None:
            if not self.selected_player.handle_click((x, y)):
                self.selected_player = None

    def get_clicked_entity(self, mouse_pos):
        return next(
            (entity for entity in self.entities if entity.is_clicked(mouse_pos)),
            None,
        )

    def is_player_turn(self, entity):
        return isinstance(entity, Player) and entity == self.entities[self.current_turn]

    def select_player(self, player):
        self.selected_player = player
        player.show_actions()

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
        if self.dragging:
            x, y = pg.mouse.get_pos()
            dx, dy = x - self.drag_start[0], y - self.drag_start[1]
            self.camera.move(-dx, -dy)
            self.drag_start = (x, y)
    
    def next_turn(self):
        """
        Advances the turn.

        Args:
            None

        Returns:
            None
        """
        self.current_turn = (self.current_turn + 1) % len(self.entities)
        current_entity = self.entities[self.current_turn]
        current_entity.center_camera(self.camera)
        if isinstance(current_entity, Monster):
            current_entity.random_action()
    
    def check_game_over(self):
        """
        Checks if the game is over.

        Args:
            None

        Returns:
            None
        """
        players = [entity for entity in self.entities if isinstance(entity, Player)]
        monsters = [entity for entity in self.entities if isinstance(entity, Monster)]

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
            self.mouse_pos = pg.mouse.get_pos()
            self.check_events()
            self.update()
            self.draw()
            
if __name__ == '__main__':
    game = Game()
    game.run()