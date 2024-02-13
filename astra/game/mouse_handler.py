import pygame as pg
from astra.game.ui.type.item_tooltip import ItemTooltip
from astra.game.ui.type.info_panel import InfoPanel
from astra.objects.entities.entity import Entity
from astra.game.commands.mouse_button_down import MouseButtonDown
from astra.game.commands.mouse_button_up import MouseButtonUp
from astra.game.commands.mouse_motion import MouseMotion

class MouseHandler:
    def __init__(self, game):
        self.game = game
        self.dragging = False
        self.hovered_entity = None
        self.info_panel = InfoPanel(self.game, 20, 20)
        self.item_tooltip = ItemTooltip(self.game, 20, 20)
        self.game_logic = self.game.game_logic
        self.hovered_item = None
        self.commands = self.initialize_commands()

    def initialize_commands(self):
        return {
            pg.MOUSEBUTTONDOWN: MouseButtonDown(self),
            pg.MOUSEBUTTONUP: MouseButtonUp(self),
        }

    def set_mouse(self):
        self.mouse = pg.Surface((5, 5))
        pg.mouse.set_visible(False)
        self.mouse.fill('red')
        self.mouse_mask = pg.mask.from_surface(self.mouse)

    def update(self):
        self.mouse_pos = self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        self.info_panel.update(self.hovered_entity)

    def draw(self):
        self.game.screen.blit(self.mouse, self.mouse_pos)
        if not self.game.menus:
            self.item_tooltip.draw()
            if self.hovered_item is None:
                self.info_panel.draw()

    def handle_event(self, event):
        if command := self.commands.get(event.type):
            command.execute(event)
        elif event.type == pg.MOUSEMOTION:
            self.handle_mouse_motion()

    def handle_mouse_motion(self):
        self.hovered_entity = self.get_clicked_entity()
        inventory = self.game_logic.current_entity.inventory
        self.hovered_item = inventory.get_item_at(self.mouse_pos)
        self.item_tooltip.update(self.hovered_item)

        MouseMotion(self).handle()

    def get_clicked_entity(self):
        for obj in self.game.object_manager.objects['entity']:
            if self.is_entity_clicked(obj):
                return obj

    def is_entity_clicked(self, entity):
        if entity_mask := getattr(entity, 'entity_mask', None):
            offset = (self.mouse_x - entity.sprite_manager.x_iso + self.game.camera.x,
                      self.mouse_y - entity.sprite_manager.y_iso + self.game.camera.y)
            return entity_mask.overlap(self.mouse_mask, offset)
        return False
