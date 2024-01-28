import pygame as pg
from monster import *
from moveIndicator import *
from attackIndicator import *
from random import randint

class Goblin(Monster):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        self.speed = 1
        self.range = 1
        self.max_health = 20
        self.health = self.max_health
        self.damage = 5
        self.indicators = [AttackIndicator(game, self), MoveIndicator(game, self)]
        
    def load_sprites(self):
        self.sprites = []
        self.sprites.extend(
            pg.image.load(f'images/goblin/idle_d{i}.png') for i in range(1, 3)
        )
            
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
        return any((x, y, z) in indicator.actions_positions for indicator in self.indicators)