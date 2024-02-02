from game.settings import *
from entities.entity import *

class Player(Entity):
    """
    Represents a player in the game.

    This class encapsulates the behavior and attributes of a player in the game. It provides methods for loading player sprites, handling player movement, updating player state, drawing the player on the screen, and showing available actions.

    Args:
        game: The instance of the game that the player belongs to.

    Attributes:
        game: The instance of the game that the player belongs to.
        x: The x-coordinate of the player's position.
        y: The y-coordinate of the player's position.
        z: The z-coordinate of the player's position.
        current_frame: The index of the current sprite frame for animation.
        animation_time: The elapsed time for the current animation frame.
        frame_duration: The duration of each animation frame.
        speed: The movement speed of the player.
        sprites: The list of player sprites for animation.
        x_iso: The isometric x-coordinate of the player's position.
        y_iso: The isometric y-coordinate of the player's position.

    Methods:
        load_sprites: Loads player sprites for animation.
        movement: Handles player movement based on keyboard input.
        update: Updates the player's state and animation frame.
        draw: Draws the player on the screen.
        show_actions: Prints available actions around the player.
        position: Returns the current position of the player.
    """

    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)     
            
    def draw(self):
        """
        Draws the player on the game screen.

        Args:
            self: The player instance.

        Returns:
            None
        """
        for indicator in self.indicators_used:
            indicator.draw()
        super().draw()
    
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
    
    def handle_click(self, entities, mouse_pos, camera):
        """
        Handles mouse click events.

        Args:
            self: The player instance.
            mouse_pos: The position of the mouse cursor.

        Returns:
            None
        """
        for indicator in self.indicators_used:
            if indicator.is_clicked(mouse_pos):
                indicator.handle_click(entities, mouse_pos)
                indicator.actions_positions.clear()
                self.game.entity_manager.next_turn(camera)
            else:
                indicator.actions_positions.clear()
    
    def can_attack(self, entity):
        return super().can_attack(entity, Player)
    
    def move(self, x, y, z):
        super().move(x, y, z)
        if item_entity := self.game.get_item_entity_at(x, y, z):
            self.inventory.add_item(item_entity.item)
            self.game.remove_entity(item_entity)