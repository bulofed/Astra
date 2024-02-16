from astra.game.commands.command import Command

class MouseButtonUp(Command):
    def __init__(self, mouse_handler):
        self.mouse_handler = mouse_handler

    def execute(self, event):
        if event.button == 1:
            self.mouse_handler.dragging = False