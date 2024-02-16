from astra.objects.entities.monsters.monster import Monster
from astra.objects.entities.players.player import Player
from astra.objects.item.types.target_item import TargetItem

class GameLogic:
    def __init__(self):
        self.current_turn = 0
        self.current_entity = None
        self.entities = []
        self.selected_item = None
        
    def select_item(self, item):
        self.selected_item = item
        
    def use_selected_item(self, target):
        if self.selected_item is not None and issubclass(self.selected_item.__class__, TargetItem):
            current_entity = self.mouse_handler.game.game_logic.current_entity
            if current_entity.can_attack(target):
                self.selected_item.use(target)
                self.selected_item = None
        
    def set_entities(self, entities):
        self.entities = entities
        self.current_entity = self.entities[self.current_turn]

    def next_turn(self, camera):
        self.current_turn = (self.current_turn + 1) % len(self.entities)
        self.current_entity = self.entities[self.current_turn]
        self.current_entity.center_camera(camera)
        self.current_entity.random_action()

    def check_win_condition(self):
        return not any(isinstance(entity, Monster) for entity in self.entities)
    
    def check_lose_condition(self):
        return not any(isinstance(entity, Player) for entity in self.entities)
    
    def check_game_over(self):
        if self.check_win_condition():
            return "Victory: All monsters have been eliminated."
        elif self.check_lose_condition():
            return "Game Over: All players have been eliminated."
        else:
            return None