from astra.indicators.indicator import Indicator, pg
from astra.objects.block.block import Block
from astra.indicators.type.indicator_object import IndicatorObject
import itertools

class MoveIndicator(Indicator):
    def __init__(self, entity):
        self.indicator = pg.image.load('astra/assets/images/indicators/move.png')
        super().__init__(entity.game, entity)

    def search_actions(self):
        for dx, dy, dz in self._get_position_range():
            self._check_and_append_position(dx, dy, dz)
        self.game.add_object(IndicatorObject(self.game, self.entity, self.entity.x, self.entity.y, self.entity.z, self.indicator))

    def _get_position_range(self):
        return itertools.product(range(-self.entity.properties.speed, self.entity.properties.speed + 1), 
                                range(-self.entity.properties.speed, self.entity.properties.speed + 1), 
                                range(-1, 2))

    def _check_and_append_position(self, dx, dy, dz):
        x, y, z = self.entity.x + dx, self.entity.y + dy, self.entity.z - 1 + dz
        block = self.game.get_object(x, y, z, type=Block)
        block_above = self.game.get_object(x, y, z + 1, type=Block)
        if block and block.solid and (not block_above or not block_above.solid):
            self.game.add_object(IndicatorObject(self.game, self.entity, x, y, z, self.indicator))
        
    def handle_action(self, x, y, z):
        self.entity.move(x, y, z + 1)