from astra.game.common.settings import SPRITE_WIDTH, SPRITE_HEIGHT
from astra.objects.object import Object, pg, calculate_isometric_position

class IndicatorObject(Object):
    def __init__(self, game, entity, x, y, z, indicator, type):
        super().__init__(game, x, y, z)
        self.entity = entity
        self.indicator = indicator
        self.type = type
        self.indicator_mask = pg.mask.from_surface(indicator)

    def draw(self, camera):
        indicator_resized = pg.transform.scale(
            self.indicator,
            (int(SPRITE_WIDTH * camera.zoom), int(SPRITE_HEIGHT * camera.zoom))
        )
        self.indicator_mask = pg.mask.from_surface(indicator_resized)
    
        self.x_iso, self.y_iso = calculate_isometric_position(self.x, self.y, self.z, camera.zoom)
        
        self.game.screen.blit(indicator_resized, (self.x_iso - camera.x, self.y_iso - camera.y))
        
    def handle_click(self):
        self.type.handle_action(self.x, self.y, self.z)
        for action in list(self.game.object_manager.get_objects(IndicatorObject)):
            self.game.object_manager.remove_object(action)
        self.game.game_logic.next_turn(self.game.camera)
        
        
    def update(self):
        pass