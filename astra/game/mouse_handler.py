import pygame as pg
from astra.game.ui.type.item_tooltip import ItemTooltip
from astra.game.ui.type.info_panel import InfoPanel
from astra.objects.entities.players.player import Player
from astra.objects.item.item import Item
from astra.objects.entities.entity import Entity
from astra.indicators.type.indicator_object import IndicatorObject

class MouseHandler:
    def __init__(self, game):
        self.game = game
        self.dragging = False
        self.selected_player = None
        self.selected_entity = None
        self.info_panel = InfoPanel(self.game, 20, 20)
        self.item_tooltip = ItemTooltip(self.game, 20, 20)
        self.game_logic = self.game.game_logic
        self.hovered_item = None
        
    def set_mouse(self):
        self.mouse = pg.Surface((5, 5))
        pg.mouse.set_visible(False)
        self.mouse.fill('red')
        self.mouse_mask = pg.mask.from_surface(self.mouse)
        
    def update(self):
        self.mouse_pos = self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        self.info_panel.update(self.selected_entity)
        self.game_logic = self.game.game_logic
        
    def draw(self):
        self.game.screen.blit(self.mouse, self.mouse_pos)
        if not self.game.menus:
            self.item_tooltip.draw()
            self.info_panel.draw() if self.hovered_item is None else None

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.handle_mouse_button_down(event)
        elif event.type == pg.MOUSEBUTTONUP:
            self.handle_mouse_button_up(event)
        elif event.type == pg.MOUSEMOTION:
            self.handle_mouse_motion()
            
    def handle_mouse_button_down(self, event):
        if event.button == 1:
            self.handle_left_click()
            self.dragging = True
            self.drag_start = self.mouse_pos
        elif event.button in [4, 5]:
            self.adjust_zoom(event.button)
            
    def handle_left_click(self):
        clicked_entity = self.get_clicked_entity()
        
        if self.hovered_item is not None:
            self.hovered_item.use(self.game_logic.current_entity)

        if self.selected_player is None and self.is_player_turn(clicked_entity):
            self.select_player(clicked_entity)
            
        elif self.selected_player:
            selected_indicator = self.get_clicked_indicator()
            selected_indicator.handle_click()
            for obj in list(self.game.objects):
                if isinstance(obj, IndicatorObject):
                    self.game.remove_object(obj)
            self.selected_player = None
                
    def handle_mouse_button_up(self, event):
        if event.button == 1:
            self.dragging = False
            
    def handle_mouse_motion(self):
        self.selected_entity = self.get_clicked_entity()
        self.hovered_item = self.game_logic.current_entity.inventory.get_item_at(self.mouse_pos)
        self.item_tooltip.update(self.hovered_item)
        
        if self.dragging:
            dx, dy = self.mouse_x - self.drag_start[0], self.mouse_y - self.drag_start[1]
            self.game.camera.move(-dx, -dy)
            self.drag_start = (self.mouse_x, self.mouse_y)
            
    def adjust_zoom(self, button):
        zoom_adjustment = .5 if button == 4 else -.5
        self.game.camera.set_zoom(self.game.camera.zoom + zoom_adjustment)
                
    def get_clicked_entity(self):
        for obj in self.game.objects:
            if isinstance(obj, Entity) and self.is_entity_clicked(obj):
                return obj
        
    def get_clicked_indicator(self):
        for obj in self.game.objects:
            if isinstance(obj, IndicatorObject) and self.is_indicator_clicked(obj):
                return obj
        
    def is_indicator_clicked(self, indicator):
        x_iso = getattr(indicator, 'x_iso', None)
        y_iso = getattr(indicator, 'y_iso', None)
        if indicator_mask := getattr(indicator, 'indicator_mask', None):
            return indicator_mask.overlap(self.mouse_mask, (self.mouse_x - x_iso + self.game.camera.x, self.mouse_y - y_iso + self.game.camera.y))
        return False

    def is_entity_clicked(self, entity):
        if entity_mask := getattr(entity, 'entity_mask', None):
            return entity_mask.overlap(self.mouse_mask, (self.mouse_x - entity.sprite_manager.x_iso + self.game.camera.x, self.mouse_y - entity.sprite_manager.y_iso + self.game.camera.y))
        return False
        
    def select_player(self, player):
        self.selected_player = player
        player.show_actions()
        
    def get_item_entity_at(self, x, y, z):
        return next(
            (entity for entity in self.game.objects if isinstance(entity, Item)
             and entity.x == x and entity.y == y and entity.z == z),
            None,
        )
        
    def is_player_turn(self, entity):
        return isinstance(entity, Player) and entity == self.game_logic.current_entity