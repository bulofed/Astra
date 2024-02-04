from astra.game.maps.entity_spawners.i_entity_spawner import IEntitySpawner
from astra.entities.items.item_entity import ItemEntity
from astra.entities.items.type.life_potion import LifePotion
from astra.entities.players.type.swordman import Swordman
from astra.entities.players.type.archer import Archer
from astra.entities.players.type.ninja import Ninja
from astra.entities.players.type.spearman import Spearman
from astra.entities.monsters.type.goblin import Goblin

class Level0(IEntitySpawner):
    def spawn_entities(self, player):
        entity_classes = {
            "swordman": Swordman,
            "archer": Archer,
            "ninja": Ninja,
            "spearman": Spearman
        }
        
        if player in entity_classes:
            self.entities.append(entity_classes[player](self.game, 2, 2, 2))
        
        self.entities.append(Goblin(self.game, 0, 2, 2))
        self.items.append(ItemEntity(self.game, 2, 0, 2, LifePotion()))
        self.game.entity_manager.add_multiple(self.entities)
        self.game.inventory_manager.add_multiple(self.items)
        self.game.game_logic.current_entity = self.game.entity_manager.entities[0]
