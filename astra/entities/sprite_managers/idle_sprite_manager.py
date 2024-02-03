from .sprite_manager import SpriteManager, pg

class ItemSpriteManager(SpriteManager):
    def load_sprite(self):
        self.sprite = pg.image.load(f'images/items/{self.entity.name}.png')