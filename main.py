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
     
    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
    
    def update(self):
        self.player.update()
        pg.display.flip()
        self.delta =  self.clock.tick(FPS)
        pg.display.set_caption(self.map.name)
        
    def draw(self):
        self.screen.fill('black')
        self.map.draw(self.camera)
        self.player.draw()
        
    def check_events(self):
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
        pg.quit()
        sys.exit()

    def handle_mouse_button_down(self, event):
        if event.button == 1:
            self.handle_left_click()
            self.dragging = True
            self.drag_start = pg.mouse.get_pos()
        elif event.button in [4, 5]:
            self.adjust_zoom(event.button)

    def handle_left_click(self):
        x, y = pg.mouse.get_pos()
        player_rect = self.player.entity_rect
        if player_rect.collidepoint(x, y):
            self.player.show_actions()

    def adjust_zoom(self, button):
        zoom_adjustment = .5 if button == 4 else -.5
        self.camera.set_zoom(self.camera.zoom + zoom_adjustment)

    def handle_mouse_button_up(self, event):
        if event.button == 1:
            self.dragging = False

    def handle_mouse_motion(self):
        if self.dragging:
            x, y = pg.mouse.get_pos()
            dx, dy = x - self.drag_start[0], y - self.drag_start[1]
            self.camera.move(-dx, -dy)
            self.drag_start = (x, y)
        
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            
if __name__ == '__main__':
    game = Game()
    game.run()