import pygame as pg
import os
from game.settings import *
from game.utils import calculate_isometric_position

class Block:
    def __init__(self, type):
        self.type = type
        self.solid = type in [1, 2, 3, 4] # A block is solid if its type is in the list
    
class Map:
    def __init__(self, game):
        self.game = game
        self.load_map()
        self.load_block_images()
        self.world_map = {}
        self.get_map()
        
    def load_map(self):
        """
        Loads the map data from a file.
        """
        map_path = os.path.join('maps', 'stage0.json')
        with open(map_path, 'r') as f:
            self.mini_map = eval(f.read())
            
    def load_block_images(self):
        """
        Loads the images for each block type.
        """
        self.block_images = {}
        blocks_folder = os.path.join('images', 'blocks')
        
        for filename in os.listdir(blocks_folder):
            if filename.endswith('.png'):
                block_value = int(os.path.splitext(filename)[0])
                image_path = os.path.join(blocks_folder, filename)
                self.block_images[block_value] = pg.image.load(image_path)
        
    def get_map(self):
        """
        Retrieves the map data from the loaded mini map.
        """
        self.name = self.mini_map['name']
        levels = self.mini_map['levels']
        for level in levels:
            map_data = []
            for row in level['map']:
                map_row = [Block(block_type) for block_type in row]
                map_data.append(map_row)
            self.world_map[level['height']] = map_data
    
    def draw(self, camera):
        for level, map_data in self.world_map.items():
            for row_index, row in enumerate(map_data):
                for col_index, block in enumerate(row):
                    x, y = calculate_isometric_position(row_index, col_index, level, camera.zoom)

                    if block.type in self.block_images:
                        block_image = self.block_images[block.type]
                        resized_block_image = pg.transform.scale(block_image, (TILE_WIDTH * camera.zoom, TILE_HEIGHT * camera.zoom))
                        self.game.screen.blit(resized_block_image, (x - camera.x, y - camera.y))

    def get_block(self, x, y, z):
        if z in self.world_map and 0 <= x < len(self.world_map[z]) and 0 <= y < len(self.world_map[z][x]):
            return self.world_map[z][x][y]
        return None
    
    def get_entity(self, entities, x, y, z):
        return next(
            (
                entity
                for entity in entities
                if entity.x == x and entity.y == y and entity.z == z
            ),
            None,
        )
        
if __name__ == '__main__':
    mini_map = Map(None)