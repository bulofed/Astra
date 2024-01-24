from settings import *

class Camera:
    def __init__(self):
        self.x = CAMERA_X
        self.y = CAMERA_Y
        self.zoom = ZOOM

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def set_zoom(self, zoom):
        if 1.0 <= zoom <= 5.0:
            self.zoom = zoom