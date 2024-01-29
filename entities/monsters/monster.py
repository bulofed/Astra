from entities.entity import *
import random as rd

class Monster(Entity):
    def __init__(self, game, x, y, z):
        super().__init__(game, x, y, z)
        
    def random_action(self):
        for indicator in self.indicators_used:
            indicator.search_actions()

        if all_actions := [
            action
            for indicator in self.indicators_used
            for action in indicator.actions_positions
        ]:
            action = rd.choice(all_actions)

            for indicator in self.indicators_used:
                if action in indicator.actions_positions:
                    indicator.handle_action(*action)
                    break

        self.game.next_turn()
    
    def can_attack(self, entity):
        return super().can_attack(entity, Monster)