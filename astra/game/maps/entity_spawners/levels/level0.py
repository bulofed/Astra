from astra.game.maps.entity_spawners.i_entity_spawner import IEntitySpawner
from astra.objects.item.item import Item
from astra.objects.item.item_list.poison_potion import PoisonPotion
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
            self.game.object_manager.add_object(entity_classes[player](self.game, 3, 4, 3))
        
        self.game.object_manager.add_object(Goblin(self.game, 10, 3, 3))
        self.game.object_manager.add_object(Goblin(self.game, 13, 5, 3))
        self.game.object_manager.add_object(Goblin(self.game, 2, 9, 3))
        self.game.object_manager.add_object(Item(self.game, 5, 7, 3, PoisonPotion()))
        self.game.object_manager.add_object(Item(self.game, 9, 14, 3, LifePotion()))
        self.game.object_manager.add_object(Item(self.game, 12, 1, 3, LifePotion()))
