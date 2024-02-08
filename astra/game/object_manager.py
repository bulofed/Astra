from astra.objects.entities.entity import Entity
from astra.objects.indicators.indicator import Indicator

class ObjectManager:
    def __init__(self, game):
        self.objects = []
        self.game = game

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def get_objects(self, type=None):
        return [obj for obj in self.objects if type is None or isinstance(obj, type)]

    def get_object(self, x, y, z, type=None):
        return next(
            (
                obj
                for obj in self.objects
                if obj.x == x and obj.y == y and obj.z == z and (type is None or isinstance(obj, type))
            ),
            None,
        )

    def update(self):
        self.game.game_logic.set_entities(self.get_objects(Entity))
        for obj in self.objects:
            obj.update()

    def draw(self):
        entity_type_priority = {Entity: 1, Indicator: 2}
        objects = sorted(self.objects, key=lambda obj: (obj.z, entity_type_priority.get(type(obj), 3), obj.y, obj.x))
        for obj in objects:
            obj.draw(self.game.camera)