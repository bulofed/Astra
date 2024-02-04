import pygame

class Menu:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.selected = 0

    def add_button(self, button):
        self.buttons.append(button)
        
    def draw(self):
        for i, button in enumerate(self.buttons):
            color = (255, 0, 0) if i == self.selected else None
            button.draw(self.game.screen, color)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event.key)
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            self.handle_mouse(event)

    def handle_keydown(self, key):
        key_actions = {
            pygame.K_UP: lambda: setattr(self, 'selected', (self.selected - 1) % len(self.buttons)),
            pygame.K_DOWN: lambda: setattr(self, 'selected', (self.selected + 1) % len(self.buttons)),
            pygame.K_RETURN: lambda: self.buttons[self.selected].click(),
            pygame.K_ESCAPE: lambda: self.game.pop_menu(),
        }

        if key in key_actions:
            key_actions[key]()

    def handle_mouse(self, event):
        for i, button in enumerate(self.buttons):
            if button.hover(self.game.mouse_handler.mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button.click()
                else:
                    self.selected = i
                break
