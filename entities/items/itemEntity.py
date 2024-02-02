from entities.entity import *
from entities.players.player import *

class ItemEntity(Entity):
    def __init__(self, game, x, y, z, item):
        super().__init__(game, x, y, z)
        self.item = item
        
    def load_sprites(self):
        pass
    
    def draw(self):
        self.x_iso, self.y_iso = self.game.map.calculate_isometric_position(self.x, self.y, self.z, self.game.camera.zoom)
        sprite = self.item.sprite
        sprite_resized = pg.transform.scale(sprite, (int(16 * self.game.camera.zoom), int(16 * self.game.camera.zoom)))
        self.game.screen.blit(sprite_resized, (self.x_iso - self.game.camera.x + sprite_resized.get_width() // 2, self.y_iso - self.game.camera.y + sprite_resized.get_height() // 2))
    
    def update(self, entities):
        for player in entities:
            if isinstance(player, Player) and player.x == self.x and player.y == self.y and player.z == self.z:
                player.inventory.add_item(self.item)
                self.game.items.remove(self)