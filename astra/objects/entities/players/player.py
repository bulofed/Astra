from astra.objects.entities.entity import Entity

class Player(Entity):
    
    def show_actions(self):
        for indicator in self.indicators_used:
            indicator.search_actions()
    
    def can_attack(self, entity):
        return not isinstance(entity, Player)
    
    def move(self, x, y, z):
        super().move(x, y, z)
        if item_entity := self.game.mouse_handler.get_item_entity_at(x, y, z):
            self.game.object_manager.remove_object(item_entity)