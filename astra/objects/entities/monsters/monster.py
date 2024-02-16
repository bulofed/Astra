from random import choice
from astra.objects.entities.entity import Entity

class Monster(Entity):
        
    def random_action(self):
        for indicator in self.indicators_used:
            indicator.search_actions()

        if all_actions := list(self.game.object_manager.objects['indicatorobject']):
            action = choice(all_actions)
            action.handle_click()
        else:
            self.game.game_logic.next_turn(self.game.camera)
    
    def can_attack(self, entity):
        return super().can_attack(entity, Monster)