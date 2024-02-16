from astra.objects.entities.entity import Entity

class Player(Entity):
    
    def show_actions(self):
        for indicator in self.indicators_used:
            indicator.search_actions()
    
    def can_attack(self, entity):
        return not isinstance(entity, Player)