import pygame

class Menu:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.selected = 0

    def add_button(self, button):
        self.buttons.append(button)
        
    def draw(self):
        for button in self.buttons:
            if button == self.buttons[self.selected]:
                button.draw(self.game.screen, (255, 0, 0))
            else:
                button.draw(self.game.screen)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                self.buttons[self.selected].click()
            elif event.key == pygame.K_ESCAPE:
                self.game.pop_menu()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.hover(self.game.mouse_handler.mouse_pos):
                    button.click()
                    break
        elif event.type == pygame.MOUSEMOTION:
            for i, button in enumerate(self.buttons):
                if button.hover(self.game.mouse_handler.mouse_pos):
                    self.selected = i
                    break