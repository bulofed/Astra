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
        self.world_map = {}
        self.load_map()
        
    def load_map(self):
        """
        Loads the map data from a file.
        """
        map_path = os.path.join('maps', 'stage0.json')
        with open(map_path, 'r') as f:
            self.mini_map = eval(f.read())
        self.load_block_images()
            
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
        
        self.get_map()
        
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
    
    def _resize_block_image(self, block_type, zoom):
        original_image = self.block_images[block_type]
        return pg.transform.scale(original_image, (TILE_WIDTH * zoom, TILE_HEIGHT * zoom))

    def draw(self, camera):
        resized_images = self._precompute_resized_images(camera)

        for level, map_data in self.world_map.items():
            self._draw_level(level, map_data, camera, resized_images)

    def _precompute_resized_images(self, camera):
        resized_images = {}
        for block_type in self.block_images.keys():
            if (block_type, camera.zoom) not in resized_images:
                resized_images[(block_type, camera.zoom)] = self._resize_block_image(block_type, camera.zoom)
        return resized_images

    def _draw_level(self, level, map_data, camera, resized_images):
        for row_index, row in enumerate(map_data):
            for col_index, block in enumerate(row):
                self._draw_block(row_index, col_index, level, block, camera, resized_images)

    def _draw_block(self, row_index, col_index, level, block, camera, resized_images):
        x, y = calculate_isometric_position(row_index, col_index, level, camera.zoom)
        self._blit_block(resized_images[(block.type, camera.zoom)], x, y, camera)

    def _blit_block(self, image, x, y, camera):
        self.game.screen.blit(image, (x - camera.x, y - camera.y))

    def get_block(self, x, y, z):
        if z in self.world_map and 0 <= x < len(self.world_map[z]) and 0 <= y < len(self.world_map[z][x]):
            return self.world_map[z][x][y]
        return None