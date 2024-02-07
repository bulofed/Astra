class Indicator():
    def __init__(self, game, entity):
        self.game = game
        self.entity = entity
    
    def handle_click(self, mouse_handler):
        def action(position):
            self.handle_action(position.x, position.y, position.z)
        self._iterate_actions_positions(mouse_handler, action)
        self.game.selected_player = None