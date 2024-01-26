import pygame as pg
import sys
from settings import *
from maps import *
from camera import *
from player import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta = 1
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
        pg.mouse.set_visible(False)
        self.map = Map(self)
        self.player = Player(self)
        self.mouse = pg.Surface((5, 5))
        self.mouse.fill('red')
        self.mouse_mask = pg.mask.from_surface(self.mouse)
    
    def update(self):
        """
        Updates the game state.

        Args:
            None

        Returns:
            None
        """
        self.player.update()
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
        self.player.draw()
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
        """
        Handles left click events.

        Args:
            None

        Returns:
            None
        """
        x, y = pg.mouse.get_pos()
        if self.selected_player is None:
            if self.player.player_mask.overlap_area(self.mouse_mask, (x - (self.player.x_iso - self.camera.x), y - (self.player.y_iso - self.camera.y))) > 0:
                self.selected_player = self.player
                self.player.show_actions()
        else:
            self.selected_player.move_indicator.handle_click((x, y))

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