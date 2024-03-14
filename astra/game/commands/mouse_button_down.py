from astra.game.commands.command import Command
from astra.objects.entities.players.player import Player
from astra.objects.item.types.self_item import SelfItem
from astra.objects.item.types.target_item import TargetItem

class MouseButtonDown(Command):
    def __init__(self, mouse_handler):
        self.mouse_handler = mouse_handler
        self.selected_player = None

    def execute(self, event):
        if event.button == 1:
            self.handle_left_click()
            self.mouse_handler.dragging = True
            self.mouse_handler.drag_start = self.mouse_handler.mouse_pos
        elif event.button in [4, 5]:
             self.adjust_zoom(event.button)
            
    def handle_left_click(self):
        item = self.mouse_handler.hovered_item
        if item is not None:
            if issubclass(item.__class__, SelfItem):
                current_entity = self.mouse_handler.game.game_logic.current_entity
                item.use(current_entity)
            elif issubclass(item.__class__, TargetItem):
                self.mouse_handler.game.game_logic.select_item(item)
        else:
            entity = self.mouse_handler.hovered_entity
            if entity is not None:
                self.mouse_handler.game.game_logic.use_selected_item(entity)

            if self.selected_player is None and self.is_player_turn(self.mouse_handler.hovered_entity):
                self.select_player(self.mouse_handler.hovered_entity)

            elif self.selected_player:
                if selected_indicator := self.get_clicked_indicator():
                    selected_indicator.handle_click()
                self.selected_player = None
            
    def is_player_turn(self, entity):
        return isinstance(entity, Player) and entity == self.mouse_handler.game_logic.current_entity
    
    def get_clicked_indicator(self):
        for obj in self.mouse_handler.game.object_manager.objects['indicatorobject']:
            if self.is_indicator_clicked(obj):
                return obj
            
    def is_indicator_clicked(self, indicator):
        x_iso = getattr(indicator, 'x_iso', None)
        y_iso = getattr(indicator, 'y_iso', None)
        if indicator_mask := getattr(indicator, 'indicator_mask', None):
            return indicator_mask.overlap(self.mouse_handler.mouse_mask, (self.mouse_handler.mouse_x - x_iso + self.mouse_handler.game.camera.x, self.mouse_handler.mouse_y - y_iso + self.mouse_handler.game.camera.y))
        return False
    
    def adjust_zoom(self, button):
        zoom_adjustment = .5 if button == 4 else -.5
        self.mouse_handler.game.camera.set_zoom(self.mouse_handler.game.camera.zoom + zoom_adjustment)
        
    def select_player(self, player):
        self.selected_player = player
        player.show_actions()