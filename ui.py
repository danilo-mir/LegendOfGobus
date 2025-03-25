import pygame
from settings import *

class UI:
  def __init__(self):
    self.display_surface = pygame.display.get_surface()
    self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

    # Barra de vida
    self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
    self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

  def show_bar(self, current, max_amount, bg_rect, color):
    # Background da barra
    pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

    # Desenhar a barra
    ratio = current / max_amount
    current_width = bg_rect.width * ratio
    current_rect = bg_rect.copy()
    current_rect.width = current_width
    pygame.draw.rect(self.display_surface, color, current_rect)
    pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

  # Mostrar o XP
  def show_exp(self, exp):
    text_surf = self.font.render('EXP: ' + str(int(exp)), False, TEXT_COLOR)
    text_rect = text_surf.get_rect(bottomright = (WIDTH-EXP_PADDING, HEIGHT-EXP_PADDING))
    pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
    self.display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

  def display(self, player):
    self.show_bar(player.health, player.stats['max_health'], self.health_bar_rect, HEALTH_COLOR)
    self.show_bar(player.energy, player.stats['max_energy'], self.energy_bar_rect, ENERGY_COLOR)
    self.show_exp(player.exp)
