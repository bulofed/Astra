from astra.game.common.settings import CAMERA_X, CAMERA_Y, ZOOM

class Camera:
    def __init__(self):
        self.x = CAMERA_X
        self.y = CAMERA_Y
        self.zoom = ZOOM

    def move(self, dx, dy):
        """
        Moves the camera by the specified amount.

        Args:
            dx: The amount to move the camera along the x-axis.
            dy: The amount to move the camera along the y-axis.
        """
        self.x += dx
        self.y += dy

    def set_zoom(self, zoom):
        """
        Sets the zoom level of the camera.

        Args:
            zoom: The new zoom level.

        Returns:
            None
        """
        if 1.0 <= zoom <= 5.0:
            self.zoom = zoom