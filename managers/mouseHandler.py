import pygame as pg
from game.settings import *
from game.itemtooltip import ItemTooltip
from game.infopanel import InfoPanel
from entities.items.itemEntity import ItemEntity
from entities.players.player import Player

class MouseHandler:
    def __init__(self, game):
        self.game = game
        self.dragging = False
        self.selected_player = None
        self.selected_entity = None
        self.info_panel = InfoPanel(self.game, 20, 20, WIDTH, HEIGHT)
        self.item_tooltip = ItemTooltip(self.game, 20, HEIGHT - INVENTORY_Y_OFFSET - FONT_SIZE*2)
        
    def set_mouse(self):
        self.mouse = pg.Surface((5, 5))
        pg.mouse.set_visible(False)
        self.mouse.fill('red')
        self.mouse_mask = pg.mask.from_surface(self.mouse)
        
    def update(self):
        self.mouse_pos = self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        self.info_panel.update(self.selected_entity)
        self.entity_manager = self.game.entity_manager
        self.game_logic = self.game.game_logic
        
    def draw(self):
        self.game.screen.blit(self.mouse, self.mouse_pos)
        self.info_panel.draw()
        self.item_tooltip.draw()

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
        entity_manager = self.entity_manager
        camera = self.game.camera
        
        if self.hovered_item is not None:
            self.hovered_item.use(self.game_logic.current_entity)

        if self.selected_player is None and self.is_player_turn(clicked_entity):
            self.select_player(clicked_entity)
        elif self.selected_player is not None:
            if not self.selected_player.handle_click(self, entity_manager, camera):
                self.selected_player = None
                
    def handle_mouse_button_up(self, event):
        """
        Handles mouse button up events.

        Args:
            event: The mouse button up event.

        Returns:
            None
        """
        if event.button == 1:
            self.dragging = False
            
    def handle_mouse_motion(self):
        hovered_entity = self.get_clicked_entity()
        self.selected_entity = hovered_entity if hovered_entity is not None else None
        
        self.hovered_item = self.game_logic.current_entity.inventory.get_item_at(self.mouse_pos)
        if self.hovered_item is not None:
            self.item_tooltip.update(self.hovered_item)
        else:
            self.item_tooltip.update(None)
        
        if self.dragging:
            dx, dy = self.mouse_x - self.drag_start[0], self.mouse_y - self.drag_start[1]
            self.game.camera.move(-dx, -dy)
            self.drag_start = (self.mouse_x, self.mouse_y)
            
    def adjust_zoom(self, button):
        """
        Adjusts the zoom level of the camera.

        Args:
            button: The mouse button that was clicked.

        Returns:
            None
        """
        zoom_adjustment = .5 if button == 4 else -.5
        self.game.camera.set_zoom(self.game.camera.zoom + zoom_adjustment)
                
    def get_clicked_entity(self):
        return next(
            (entity for entity in self.entity_manager.entities if entity.is_clicked(self)),
            None,
        )
        
    def select_player(self, player):
        self.selected_player = player
        player.show_actions(self.entity_manager.entities)
        
    def get_item_entity_at(self, x, y, z):
        return next(
            (entity for entity in self.entity_manager.entities if isinstance(entity, ItemEntity)
             and entity.x == x and entity.y == y and entity.z == z),
            None,
        )
        
    def is_player_turn(self, entity):
        return isinstance(entity, Player) and entity == self.game_logic.current_entity