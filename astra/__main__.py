from astra import app
from astra.objects.block.block import Block

if __name__ == "__main__":
    game = app.Game()
    Block.load_block_images()
    game.run()