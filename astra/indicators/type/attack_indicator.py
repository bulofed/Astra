from astra.indicators.indicator import Indicator, pg
from astra.indicators.type.indicator_object import IndicatorObject
import itertools

class AttackIndicator(Indicator):
    def __init__(self, entity):
        self.indicator = pg.image.load('astra/assets/images/indicators/attack.png') 
        super().__init__(entity.game, entity)

    def search_actions(self):
        for dx, dy, dz in itertools.product(range(-self.entity.properties.speed, self.entity.properties.speed + 1), 
                                range(-self.entity.properties.speed, self.entity.properties.speed + 1), 
                                range(-1, 2)):
            x, y, z = self.entity.x + dx, self.entity.y + dy, self.entity.z + dz
            enemy = self.game.get_entity(x, y, z)
            if enemy and enemy != self.entity and self.entity.can_attack(enemy):
                self.x = x
                self.y = y
                self.z = z - 1
                self.game.add_object(IndicatorObject(self.game, self.entity, self.x, self.y, self.z, self.indicator, self))

    def handle_action(self, x, y, z):
        enemy = self.game.get_entity(x, y, z + 1)
        self.entity.attack(enemy)

    def has_possible_actions(self):
        return bool(self.actions_positions)