from astra.entities.entity import EntityProperties
from astra.entities.players.player import Player

class Ninja(Player):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z, EntityProperties(2, (0,1), 10, 4))