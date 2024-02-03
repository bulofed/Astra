from astra.entities.players.player import Player

class Swordman(Player):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        self.speed = 1
        self.range = 1
        self.max_health = 20
        self.health = self.max_health
        self.damage = 5