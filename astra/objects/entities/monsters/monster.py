from random import choice
from astra.objects.entities.entity import Entity
from astra.objects.indicators.indicator_object import IndicatorObject

class Monster(Entity):
        
    def random_action(self):
        for indicator in self.indicators_used:
            indicator.search_actions()

        if all_actions := list(self.game.object_manager.get_objects(IndicatorObject)):
            action = choice(all_actions)
            action.handle_click()
        else:
            self.game.game_logic.next_turn(self.game.camera)
    
    def can_attack(self, entity):
        return super().can_attack(entity, Monster)