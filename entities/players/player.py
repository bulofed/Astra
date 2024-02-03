from game.settings import *
from entities.entity import *

class Player(Entity):

    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)     
    
    def show_actions(self, entities):
        """
        Shows the available actions for the player.

        Args:
            self: The player instance.

        Returns:
            None
        """
        for indicator in self.indicators_used:
            if isinstance(indicator, MoveIndicator):
                indicator.search_actions()
            elif isinstance(indicator, AttackIndicator):
                indicator.search_actions(entities)
    
    def handle_click(self, mouse_handler, entity_manager, camera):
        """
        Handles mouse click events.

        Args:
            self: The player instance.
            mouse_pos: The position of the mouse cursor.

        Returns:
            None
        """
        for indicator in self.indicators_used:
            if indicator.is_clicked(mouse_handler):
                indicator.handle_click(entity_manager, mouse_handler)
                indicator.actions_positions.clear()
                self.game.game_logic.next_turn(camera)
            else:
                indicator.actions_positions.clear()
    
    def can_attack(self, entity):
        return super().can_attack(entity, Player)
    
    def move(self, x, y, z):
        super().move(x, y, z)
        if item_entity := self.game.mouse_handler.get_item_entity_at(x, y, z):
            self.game.remove_entity(item_entity)