from astra.objects.entities.entity import Entity

class Player(Entity):
    
    def show_actions(self):
        for indicator in self.indicators_used:
                indicator.search_actions()
    
    def handle_click(self, mouse_handler, camera):
        for indicator in self.indicators_used:
            indicator.handle_click(mouse_handler)
            indicator.actions_positions.clear()
        self.game.game_logic.next_turn(camera)
    
    def can_attack(self, entity):
        return not isinstance(entity, Player)
    
    def move(self, x, y, z):
        super().move(x, y, z)
        if item_entity := self.game.mouse_handler.get_item_entity_at(x, y, z):
            self.game.remove_object(item_entity)