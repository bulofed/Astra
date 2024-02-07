from astra.objects.entities.entity import EntityProperties
from astra.objects.entities.players.player import Player

class Swordman(Player):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z, EntityProperties(1, (0,1), 20, 5))