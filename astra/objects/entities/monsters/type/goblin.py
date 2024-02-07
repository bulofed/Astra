from astra.objects.entities.monsters.monster import Monster
from astra.objects.entities.entity import EntityProperties


class Goblin(Monster):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z, EntityProperties(1, (0, 1), 20, 5))
