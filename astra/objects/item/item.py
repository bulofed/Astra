from astra.objects.object import Object, pg, calculate_isometric_position
from astra.game.common.settings import ITEM_WIDTH, ITEM_HEIGHT

class Item(Object):
    def __init__(self, game, x, y, z, properties):
        super().__init__(game, x, y, z)
        self.is_hidden = False
        self.properties = properties
        
    def draw(self, camera):
        x, y = calculate_isometric_position(self.x, self.y, self.z, camera.zoom)
        
        screen_x = x - camera.x
        screen_y = y - camera.y
        
        offset_x = ITEM_WIDTH * camera.zoom
        offset_y = ITEM_HEIGHT * camera.zoom
        
        if -offset_x <= screen_x <= camera.width + offset_x and -offset_y <= screen_y <= camera.height + offset_y:
            zoomed_item = pg.transform.scale(self.properties.sprite, (int(ITEM_WIDTH * camera.zoom), int(ITEM_HEIGHT * camera.zoom)))
            self.game.screen.blit(zoomed_item, (x - camera.x + zoomed_item.get_width() // 2, y - camera.y + zoomed_item.get_height() // 2))
    
    def update(self):
        for player in self.game.object_manager.objects['entity']:
            if player.x == self.x and player.y == self.y and player.z == self.z:
                player.inventory.add_item(self.properties)
                self.game.object_manager.remove_object(self)
                break