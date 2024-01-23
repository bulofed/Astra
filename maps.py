import pygame as pg
import os
from settings import *

class Map:
    def __init__(self, game):
        self.game = game
        self.load_map()
        self.load_block_images()
        self.world_map = {}
        self.get_map()
        
    def load_map(self):
        map_path = os.path.join('maps', 'stage0.json')
        with open(map_path, 'r') as f:
            self.mini_map = eval(f.read())
            
    def load_block_images(self):
        self.block_images = {}
        blocks_folder = os.path.join('images', 'blocks')
        
        for filename in os.listdir(blocks_folder):
            if filename.endswith('.png'):
                block_value = int(os.path.splitext(filename)[0])
                image_path = os.path.join(blocks_folder, filename)
                self.block_images[block_value] = pg.image.load(image_path)
        
    def get_map(self):
        self.name = self.mini_map['name']
        levels = self.mini_map['levels']
        for level in levels:
            self.world_map[level['height']] = level['map']
    
    def calculate_isometric_position(self, x, y, z):
        tile_width = 32
        tile_height = 32
        iso_x_factor = .5
        iso_y_factor = .25
        return (x - y) * tile_width * iso_x_factor + WIDTH/2, (x + y - z) * tile_height * iso_y_factor + HEIGHT/2
    
    def draw(self):
        for level, map_data in self.world_map.items():
            for row_index, row in enumerate(map_data):
                for col_index, block_type in enumerate(row):
                    x, y = self.calculate_isometric_position(row_index, col_index, level)

                    if block_type in self.block_images:
                        block_image = self.block_images[block_type]
                        resized_block_image = pg.transform.scale(block_image, (TILE_WIDTH, TILE_HEIGHT))
                        self.game.screen.blit(resized_block_image, (x, y))
        
if __name__ == '__main__':
    mini_map = Map(None)