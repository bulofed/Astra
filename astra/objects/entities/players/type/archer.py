from astra.objects.entities.entity import EntityProperties
from astra.objects.entities.players.player import Player

class Archer(Player):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z, EntityProperties(1, (2,3), 15, 3))