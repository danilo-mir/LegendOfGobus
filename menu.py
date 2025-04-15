# menu.py

import pygame
import sys
from settings import *

class Button:
    def __init__(self, text, pos, size, font, bg_color, border_color, border_thickness=5):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.font = font
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_thickness = border_thickness

    def draw(self, surface, hover=False):
        new_rect = self.rect.inflate(self.rect.width * 0.05, self.rect.height * 0.05) if hover else self.rect
        pygame.draw.rect(surface, self.bg_color, new_rect)
        pygame.draw.rect(surface, self.border_color, new_rect, self.border_thickness)

        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=new_rect.center)
        surface.blit(text_surface, text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.is_hovered(mouse_pos) and mouse_pressed[0]


class Slider:
    def __init__(self, pos, width, initial_value=50):
        self.rect = pygame.Rect(pos[0], pos[1], width, 20)
        self.value = initial_value
        self.dragging = False

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        knob_x = self.rect.x + (self.value / 100) * self.rect.width - 5
        pygame.draw.rect(surface, (255, 165, 0), pygame.Rect(knob_x, self.rect.y - 5, 10, self.rect.height + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = event.pos[0] - self.rect.x
            self.value = max(0, min(100, (rel_x / self.rect.width) * 100))


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.in_options = False

        self.bg = pygame.image.load(BG)
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        self.overlay = pygame.Surface((WIDTH, HEIGHT))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(200)

        self.button_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.title_font = pygame.font.Font(UI_FONT, 30)

        self.buttons = [
            Button("Play", (WIDTH//2 - 100, 300), (200, 60), self.button_font, (255, 165, 0), (255, 255, 255)),
            Button("Options", (WIDTH//2 - 100, 380), (200, 60), self.button_font, (255, 165, 0), (255, 255, 255)),
            Button("Quit", (WIDTH//2 - 100, 460), (200, 60), self.button_font, (255, 165, 0), (255, 255, 255))
        ]
        self.back_button = Button("Back", (WIDTH//2 - 100, 400), (200, 60), self.button_font, (255, 165, 0), (255, 255, 255))

        self.slider_music = Slider((WIDTH//2 - 100, 200), 200)
        self.slider_sfx = Slider((WIDTH//2 - 100, 260), 200)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.in_options:
                self.slider_music.handle_event(event)
                self.slider_sfx.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN and self.back_button.is_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
                    self.in_options = False
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_click = pygame.mouse.get_pressed()
                    if self.buttons[0].is_clicked(mouse_pos, mouse_click):  # Play
                        self.running = False
                    elif self.buttons[1].is_clicked(mouse_pos, mouse_click):  # Options
                        self.in_options = True
                    elif self.buttons[2].is_clicked(mouse_pos, mouse_click):  # Quit
                        pygame.quit()
                        sys.exit()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.overlay, (0, 0))

        if self.in_options:
            self.slider_music.draw(self.screen)
            self.slider_sfx.draw(self.screen)
            self.back_button.draw(self.screen, self.back_button.is_hovered(pygame.mouse.get_pos()))
        else:
            title_surface = self.title_font.render("Legend of Göbus: Breath of Baphên", True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(WIDTH//2, 180))
            self.screen.blit(title_surface, title_rect)

            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.draw(self.screen, button.is_hovered(mouse_pos))

    def get_volume_settings(self):
        return self.slider_music.value, self.slider_sfx.value
