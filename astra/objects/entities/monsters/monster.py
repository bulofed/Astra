import random as rd
from astra.objects.entities.entity import Entity

class Monster(Entity):
        
    def random_action(self, entities):
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
                indicator.actions_positions.clear()
        
        self.game.game_logic.next_turn(self.game.camera)
    
    def can_attack(self, entity):
        return super().can_attack(entity, Monster)