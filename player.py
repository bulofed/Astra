from settings import *
from entity import *
from moveIndicator import *
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

    def __init__(self, game):
        self.game = game
        self.x, self.y, self.z = PLAYER_POS
        self.current_frame = 0
        self.animation_time = 0
        self.frame_duration = .5
        self.speed = 1
        self.load_sprites()
        self.move_indicator = MoveIndicator(self.game, self)
    
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
        
    def update(self):
        """
        Updates the player's state and animation.

        Args:
            self: The player instance.

        Returns:
            None
        """
        self.animation_time += self.game.delta / 1000
        if self.animation_time >= self.frame_duration:
            self.animation_time -= self.frame_duration
            self.current_frame = (self.current_frame + 1) % len(self.sprites)
            
    def draw(self):
        """
        Draws the player on the game screen.

        Args:
            self: The player instance.

        Returns:
            None
        """
        self.x_iso, self.y_iso = self.game.map.calculate_isometric_position(self.x, self.y, self.z, self.game.camera.zoom)
        sprite = self.sprites[self.current_frame]
        sprite_resized = pg.transform.scale(sprite, (int(SPRITE_WIDTH * self.game.camera.zoom), int(SPRITE_HEIGHT * self.game.camera.zoom)))
        self.move_indicator.draw()
        self.game.screen.blit(sprite_resized, (self.x_iso - self.game.camera.x, self.y_iso - self.game.camera.y))
        self.player_mask = pg.mask.from_surface(sprite_resized)
    
    def show_actions(self):
        """
        Shows the available actions for the player.

        Args:
            self: The player instance.

        Returns:
            None
        """
        self.move_indicator.show_actions()
        
    def move(self, x, y, z):
        """
        Moves the player to the specified position.

        Args:
            self: The player instance.
            x: The x-coordinate of the position to move to.
            y: The y-coordinate of the position to move to.
            z: The z-coordinate of the position to move to.

        Returns:
            None
        """
        self.x, self.y, self.z = x, y, z
        
    @property
    def position(self):
        return self.x, self.y, self.z