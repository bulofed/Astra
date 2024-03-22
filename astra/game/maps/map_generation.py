import pygame as pg
import os
from astra.objects.block.block import Block
    
class Map:
    def __init__(self, game):
        self.game = game
        self.world_map = []
        
    def load_map(self, level):
        """
        Loads the map data from a file.
        """
        map_path = os.path.join('astra', 'assets', 'maps', f'stage{level}.json')
        with open(map_path, 'r') as f:
            self.mini_map = eval(f.read())
        self.load_block_images()
            
    def load_block_images(self):
        """
        Loads the images for each block type.
        """
        self.block_images = {}
        blocks_folder = os.path.join('astra', 'assets', 'images', 'blocks')
        
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
        for z, level in enumerate(levels):
            for y, row in enumerate(level['map']):
                for x, block_type in enumerate(row):
                    if block_type != 0:
                        block = Block(self.game, x, y, z, block_type)
                        self.game.object_manager.add_object(block)
                        self.world_map.append(block)
        self.world_map.sort(key=lambda block: (block.y, block.x, -block.z))
        self.mark_hidden_blocks()

    def mark_hidden_blocks(self):
        """
        Marks blocks that are hidden by other blocks.
        """
        last_block = None
        for block in self.world_map:
            block.is_hidden = (
                last_block is not None
                and block.x == last_block.x
                and block.y == last_block.y
                and block.z <= last_block.z
            )
            last_block = block