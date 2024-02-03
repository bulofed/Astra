class SpriteManagerFactory:
    _registry = {}

    @staticmethod
    def register(entity_type, sprite_manager_type):
        SpriteManagerFactory._registry[entity_type] = sprite_manager_type

    @staticmethod
    def create(entity):
        entity_type = entity.get_sprite_manager_type()
        if entity_type not in SpriteManagerFactory._registry:
            raise ValueError(f"No sprite manager registered for entity type {entity_type}")
        sprite_manager_type = SpriteManagerFactory._registry[entity_type]
        return sprite_manager_type(entity)