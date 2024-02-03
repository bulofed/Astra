from astra.indicators.indicator import Indicator, pg
import itertools

class MoveIndicator(Indicator):
    def __init__(self, game, entity):
        indicator = pg.image.load('astra/assets/images/indicators/move.png')
        super().__init__(game, entity, indicator)

    def search_actions(self):
        self.actions_positions.clear()
        for dx, dy, dz in self._get_position_range():
            self._check_and_append_position(dx, dy, dz)

    def _get_position_range(self):
        return itertools.product(range(-self.entity.speed, self.entity.speed + 1), 
                                range(-self.entity.speed, self.entity.speed + 1), 
                                range(-1, 2))

    def _check_and_append_position(self, dx, dy, dz):
        x, y, z = self.entity.x + dx, self.entity.y + dy, self.entity.z - 1 + dz
        block = self.game.map.get_block(x, y, z)
        block_above = self.game.map.get_block(x, y, z + 1)
        if block and block.solid and not block_above and not self.entity.is_position_occupied(x, y, z):
            self.actions_positions.append((x, y, z))
        
    def handle_action(self, _, x, y, z):
        self.entity.move(x, y, z + 1)