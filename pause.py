import pygame
import sys
from menu import *
from settings import *

class PauseScreen:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load(BG)
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        self.overlay = pygame.Surface((WIDTH, HEIGHT))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(200)
        self.button_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE + 20)
        self.buttons = [
            Button("Resume", (WIDTH//2 - 100, 300), (200, 60), self.button_font, (255, 165, 0), (255, 255, 255)),
            Button("Menu", (WIDTH//2 - 100, 380), (200, 60), self.button_font, (255, 165, 0), (255, 255, 255)),
            Button("Quit", (WIDTH//2 - 100, 460), (200, 60), self.button_font, (255, 165, 0), (255, 255, 255))
        ]
        
    def run(self):
        while True:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
            
            if not self.game.game_paused:
                break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()

                if self.buttons[0].is_clicked(mouse_pos, mouse_click):
                    self.game.game_paused = False
                    return

                elif self.buttons[1].is_clicked(mouse_pos, mouse_click):
                    self.game.game_paused = False
                    menu = Menu(self.screen)
                    menu.run()
                    self.game.game_paused = False
                    return

                elif self.buttons[2].is_clicked(mouse_pos, mouse_click):
                    pygame.quit()
                    sys.exit()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.overlay, (0, 0))
        title_surface = self.title_font.render("Game Paused", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH//2, 180))
        self.screen.blit(title_surface, title_rect)
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, button.is_hovered(mouse_pos))
