from astra.entities.type.animated_entity import AnimatedEntity
from astra.indicators.type.attack_indicator import AttackIndicator
from astra.indicators.type.move_indicator import MoveIndicator

class Player(AnimatedEntity):
    
    def show_actions(self, entities):
        for indicator in self.indicators_used:
            if isinstance(indicator, MoveIndicator):
                indicator.search_actions()
            elif isinstance(indicator, AttackIndicator):
                indicator.search_actions(entities)
    
    def handle_click(self, mouse_handler, entity_manager, camera):
        for indicator in self.indicators_used:
            indicator.handle_click(entity_manager, mouse_handler)
            indicator.actions_positions.clear()
        self.game.game_logic.next_turn(camera)
    
    def can_attack(self, entity):
        return super().can_attack(entity, Player)
    
    def move(self, x, y, z):
        super().move(x, y, z)
        if item_entity := self.game.mouse_handler.get_item_entity_at(x, y, z):
            self.game.remove_entity(item_entity)