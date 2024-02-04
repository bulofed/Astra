from astra.entities.entity import EntityProperties
from astra.entities.players.player import Player

class Spearman(Player):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z, EntityProperties(1, (0,2), 15, 4))