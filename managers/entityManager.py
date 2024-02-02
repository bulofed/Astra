from entities.monsters.monster import *

class EntityManager():
    def __init__(self):
        self.entities = []
        self.current_turn = 0
        self.current_entity = None
        
    def add_entity(self, entity):
        self.entities.append(entity)
        
    def remove_entity(self, entity):
        self.entities.remove(entity)
        
    def update_entities(self):
        for entity in self.entities:
            entity.update()
    
    def draw_entities(self):
        for entity in self.entities:
            entity.draw()
            
    def next_turn(self, camera):
        self.current_turn = (self.current_turn + 1) % len(self.entities)
        self.current_entity = self.entities[self.current_turn]
        self.current_entity.center_camera(camera)
        if isinstance(self.current_entity, Monster):
            self.current_entity.random_action(self)