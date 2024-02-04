from astra.game.common.settings import WIDTH, HEIGHT, TILE_WIDTH, TILE_HEIGHT

def calculate_isometric_position(x, y, z, zoom):
        obj_width = TILE_WIDTH * zoom
        obj_height = TILE_HEIGHT * zoom
        iso_x_factor = .5
        iso_y_factor = .25
        return (y - x) * obj_width * iso_x_factor + WIDTH/2, (x + y - z*2) * obj_height * iso_y_factor + HEIGHT/2

def get_entity(entities, x, y, z):
    return next(
        (
            entity
            for entity in entities
            if entity.x == x and entity.y == y and entity.z == z
        ),
        None,
    )
    
def is_position_occupied(entities, x, y, z):
    return any(entity.x == x and entity.y == y and entity.z == z + 1 for entity in entities)