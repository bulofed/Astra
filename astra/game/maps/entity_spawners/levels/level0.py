from astra.game.maps.entity_spawners.i_entity_spawner import IEntitySpawner
from astra.objects.item.item import Item
from astra.objects.item.item_list.life_potion import LifePotion
from astra.objects.entities.players.type.swordman import Swordman
from astra.objects.entities.players.type.archer import Archer
from astra.objects.entities.players.type.ninja import Ninja
from astra.objects.entities.players.type.spearman import Spearman
from astra.objects.entities.monsters.type.goblin import Goblin

class Level0(IEntitySpawner):
    def spawn_entities(self, player):
        entity_classes = {
            "swordman": Swordman,
            "archer": Archer,
            "ninja": Ninja,
            "spearman": Spearman
        }
        
        if player in entity_classes:
            self.game.add_object(entity_classes[player](self.game, 1, 1, 1))
        
        self.game.add_object(Goblin(self.game, 2, 2, 1))
