from astra.game.common.settings import SPRITE_WIDTH, SPRITE_HEIGHT
from astra.objects.object import Object, pg, calculate_isometric_position

class IndicatorObject(Object):
    def __init__(self, game, entity, x, y, z, indicator, type):
        super().__init__(game, x, y, z)
        self.is_hidden = False
        self.entity = entity
        self.indicator = indicator
        self.type = type
        self.indicator_mask = pg.mask.from_surface(indicator)

    def draw(self, camera):
        self.x_iso, self.y_iso = calculate_isometric_position(self.x, self.y, self.z, camera.zoom)
        screen_x = self.x_iso - camera.x
        screen_y = self.y_iso - camera.y

        offset_x = SPRITE_WIDTH * camera.zoom
        offset_y = SPRITE_HEIGHT * camera.zoom

        if -offset_x <= screen_x <= camera.width + offset_x and -offset_y <= screen_y <= camera.height + offset_y:
            indicator_resized = pg.transform.scale(
                self.indicator,
                (int(SPRITE_WIDTH * camera.zoom), int(SPRITE_HEIGHT * camera.zoom))
            )
            self.indicator_mask = pg.mask.from_surface(indicator_resized)
            self.game.screen.blit(indicator_resized, (self.x_iso - camera.x, self.y_iso - camera.y))
        
    def handle_click(self):
        self.type.handle_action(self.x, self.y, self.z)
        self.game.object_manager.remove_objects('indicatorobject')
        self.game.game_logic.next_turn(self.game.camera)
        
        
    def update(self):
        pass