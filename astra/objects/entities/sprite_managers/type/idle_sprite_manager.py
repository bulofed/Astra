from ..sprite_manager import SpriteManager, pg

class IdleSpriteManager(SpriteManager):
    def load_sprite(self):
        self.sprite = pg.image.load(f'images/items/{self.entity.name}.png')