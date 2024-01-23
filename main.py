import pygame as pg
import sys
from settings import *
from maps import *
from camera import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.new_game()
        self.camera = Camera()
        self.dragging = False
     
    def new_game(self):
        self.map = Map(self)
    
    def update(self):
        pg.display.flip()
        self.clock.tick(FPS)
        pg.display.set_caption(self.map.name)
        
    def draw(self):
        self.screen.fill('black')
        self.map.draw(self.camera)
        
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.dragging = True
                    self.drag_start = pg.mouse.get_pos()
                elif event.button == 4:
                    self.camera.set_zoom(self.camera.zoom + .5)
                elif event.button == 5:
                    self.camera.set_zoom(self.camera.zoom - .5)
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            elif event.type == pg.MOUSEMOTION:
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