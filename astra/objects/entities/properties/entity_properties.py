class EntityProperties:
    def __init__(self, speed=1, range=(0,1), max_health=20, damage=5):
        self.speed = speed
        self.range = range
        self.max_health = max_health
        self.health = max_health
        self.damage = damage
        self.poisoned = 0
        self.poison_amount = 0