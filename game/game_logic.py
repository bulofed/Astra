from entities.monsters.monster import Monster
from entities.players.player import Player
from game.settings import *

class GameLogic:
    def __init__(self, entity_manager):
        self.entity_manager = entity_manager
        self.entities = entity_manager.entities
        self.current_turn = 0
        self.current_entity = self.entities[self.current_turn]

    def next_turn(self, camera):
        self.current_turn = (self.current_turn + 1) % len(self.entities)
        self.current_entity = self.entities[self.current_turn]
        self.current_entity.center_camera(camera)
        self.current_entity.random_action(self.entity_manager)

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