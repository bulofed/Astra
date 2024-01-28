from game.settings import *
from entities.entity import *
import pygame as pg

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
        self.speed = 1
        self.range = 1
        self.max_health = 20
        self.health = self.max_health
        self.damage = 5      
    
    def load_sprites(self):
        """
        Loads player sprites.

        This method loads player sprites for idle animation. It populates the `sprites` attribute of the instance with the loaded images.

        Args:
            self: The instance of the class.

        Returns:
            None
        """

        self.sprites = []
        self.sprites.extend(
            pg.image.load(f'images/player/idle_d{i}.png') for i in range(1, 3)
        )
            
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
    
    def show_actions(self):
        """
        Shows the available actions for the player.

        Args:
            self: The player instance.

        Returns:
            None
        """
        for indicator in self.indicators_used:
            indicator.search_actions()
    
    def handle_click(self, mouse_pos):
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
                indicator.handle_click(mouse_pos)
                indicator.actions_positions.clear()
                self.game.next_turn()
            else:
                indicator.actions_positions.clear()
    
    def is_position_occupied(self, x, y, z):
        """
        Checks if the specified position is occupied.

        Args:
            self: The player instance.
            x: The x-coordinate of the position to check.
            y: The y-coordinate of the position to check.
            z: The z-coordinate of the position to check.

        Returns:
            True if the position is occupied, False otherwise.
        """
        return any((x, y, z) in indicator.actions_positions for indicator in self.indicators_used)
    
    def can_attack(self, entity):
        return super().can_attack(entity, Player)