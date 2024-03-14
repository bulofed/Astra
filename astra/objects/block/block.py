from astra.objects.object import Object, pg, calculate_isometric_position
import os
from astra.game.common.settings import TILE_WIDTH, TILE_HEIGHT

class Block(Object):
    block_images = {}
    
    @classmethod
    def load_block_images(cls):
        """Loads the images for each block type."""
        cls.block_images = {}
        blocks_folder = os.path.join('astra', 'assets', 'images', 'blocks')
        
        for filename in os.listdir(blocks_folder):
            if filename.endswith('.png'):
                block_value = int(os.path.splitext(filename)[0])
                image_path = os.path.join(blocks_folder, filename)
                image = pg.image.load(image_path)
                cls.block_images[block_value] = image
    
    def __init__(self, game, x, y, z, type):
        """A block is used to represent a tile in the game world."""
        super().__init__(game, x, y, z)
        self.type = type
        self.solid = type in [1, 2, 3, 4] # A block is solid if its type is in the list
        
    def draw(self, camera):
        """Draws the block on the screen."""
        x, y = calculate_isometric_position(self.x, self.y, self.z, camera.zoom)
        screen_x = x - camera.x
        screen_y = y - camera.y
        offset_x = TILE_WIDTH * camera.zoom
        offset_y = TILE_HEIGHT * camera.zoom
        
        if -offset_x <= screen_x <= camera.width + offset_x and -offset_y <= screen_y <= camera.height + offset_y:
            image_zoomed = pg.transform.scale(self.block_images[self.type], (int(TILE_WIDTH * camera.zoom), int(TILE_HEIGHT * camera.zoom)))
            self.game.screen.blit(image_zoomed, (x - camera.x, y - camera.y))
        
    def update(self):
        pass
        