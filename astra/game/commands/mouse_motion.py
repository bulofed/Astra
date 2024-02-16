class MouseMotion:
    def __init__(self, mouse_handler):
        self.mouse_handler = mouse_handler

    def handle(self):
        if self.mouse_handler.dragging:
            self.handle_dragging()

    def handle_dragging(self):
        dx, dy = self.mouse_handler.mouse_x - self.mouse_handler.drag_start[0], self.mouse_handler.mouse_y - self.mouse_handler.drag_start[1]
        self.mouse_handler.game.camera.move(-dx, -dy)
        self.mouse_handler.drag_start = (self.mouse_handler.mouse_x, self.mouse_handler.mouse_y)