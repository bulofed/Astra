import random as rd
from astra.entities.type.animated_entity import AnimatedEntity
from astra.indicators.type.attack_indicator import AttackIndicator
from astra.indicators.type.move_indicator import MoveIndicator

class Monster(AnimatedEntity):
        
    def random_action(self, entity_manager):
        for indicator in self.indicators_used:
            if isinstance(indicator, MoveIndicator):
                indicator.search_actions()
            elif isinstance(indicator, AttackIndicator):
                indicator.search_actions(entity_manager.entities)

        if all_actions := [
            action
            for indicator in self.indicators_used
            for action in indicator.actions_positions
        ]:
            action = rd.choice(all_actions)

            for indicator in self.indicators_used:
                if action in indicator.actions_positions:
                    indicator.handle_action(entity_manager, *action)
                indicator.actions_positions.clear()
        
        self.game.game_logic.next_turn(self.game.camera)
    
    def can_attack(self, entity):
        return super().can_attack(entity, Monster)