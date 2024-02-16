from astra.objects.entities.entity import Entity
from astra.objects.indicators.indicator import Indicator
from astra.objects.object import Object

class ObjectManager:
    def __init__(self, game):
        self.objects = {}
        self.game = game

    def add_object(self, obj):
        mro = type(obj).mro()
        if Object in mro:
            obj_type = mro[mro.index(Object) - 1].__name__.lower()
        else:
            obj_type = type(obj).__name__.lower()
        if obj_type not in self.objects:
            self.objects[obj_type] = []
        self.objects[obj_type].append(obj)

    def remove_object(self, obj):
        mro = type(obj).mro()
        if Object in mro:
            obj_type = mro[mro.index(Object) - 1].__name__.lower()
        else:
            obj_type = type(obj).__name__.lower()
        if obj_type in self.objects:
            self.objects[obj_type].remove(obj)

    def remove_objects(self, type):
        if type in self.objects:
            del self.objects[type]

    def get_objects(self, type=None):
        if type is None:
            return [obj for obj_list in self.objects.values() for obj in obj_list]
        else:
            return [obj for obj_type, obj_list in self.objects.items() if issubclass(obj_type, type) for obj in obj_list]

    def get_object(self, x, y, z, type=None):
        objects = self.get_objects() if type is None else self.objects[type]
        return next(
            (
                obj
                for obj in objects
                if obj.x == x and obj.y == y and obj.z == z
            ),
            None,
        )

    def update(self):
        self.game.game_logic.set_entities(self.objects['entity'])
        for obj_list in self.objects.values():
            for obj in obj_list:
                obj.update()

    def draw(self):
        entity_type_priority = {Entity: 1, Indicator: 2}
        objects = sorted(self.get_objects(), key=lambda obj: (obj.z, entity_type_priority.get(type(obj), 3), obj.y, obj.x))
        for obj in objects:
            obj.draw(self.game.camera)