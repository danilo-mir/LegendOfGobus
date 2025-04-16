import pygame
import sys
from settings import *
from menu import Button

class DeathScreen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.should_reset_level = False  # Indica se o nivel deve ser recriado
        
        # Fundo
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.fill((0, 0, 0))  # Fundo preto
        
        # Fontes
        self.title_font = pygame.font.Font(UI_FONT, 80)
        self.button_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        # Botões
        self.buttons = [
            Button("Reiniciar", (WIDTH//2 - 100, HEIGHT//2 + 50), (200, 60), self.button_font, (255, 165, 0), (255, 255, 255)),
            Button("Sair", (WIDTH//2 - 100, HEIGHT//2 + 130), (200, 60), self.button_font, (255, 165, 0), (255, 255, 255))
        ]

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        return self.should_reset_level  # Retorna se o nivel deve ser recriado

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()
                
                if self.buttons[0].is_clicked(mouse_pos, mouse_click):  # Reiniciar
                    self.running = False
                    self.should_reset_level = True  # Sinaliza que o nivel deve ser recriado
                    return
                
                if self.buttons[1].is_clicked(mouse_pos, mouse_click):  # Sair
                    pygame.quit()
                    sys.exit()

    def draw(self):
        # Desenhar fundo
        self.screen.blit(self.bg, (0, 0))
        
        # Desenhar título "FOI DE GELAS"
        title_surf = self.title_font.render("FOI DE GELAS", True, (255, 0, 0))
        title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
        self.screen.blit(title_surf, title_rect)
        
        # Desenhar subtitulo
        subtitle_surf = self.button_font.render("Voce morreu!", True, (255, 255, 255))
        subtitle_rect = subtitle_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.screen.blit(subtitle_surf, subtitle_rect)
        
        # Desenhar botões
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, button.is_hovered(mouse_pos)) 