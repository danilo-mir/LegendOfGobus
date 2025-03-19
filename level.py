import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
  def __init__(self):
    # Acesso à variável da tela
    self.display_surface = pygame.display.get_surface()
    
    # Criar grupos de sprites
    self.visibile_sprites = pygame.sprite.Group()
    self.obstacle_sprites = pygame.sprite.Group()

    # Criar sprite do mapa
    self.create_map()

  def create_map(self):
    for row_index, row in enumerate(WORLD_MAP):
      for col_index, col in enumerate(row):
        x = col_index * TILESIZE
        y = row_index * TILESIZE
        if col == 'R':
          Tile((x, y), [self.visibile_sprites, self.obstacle_sprites])
        if col == 'P':
          Player((x, y), [self.visibile_sprites], self.obstacle_sprites)


  def run(self):
    self.visibile_sprites.draw(self.display_surface)
    self.visibile_sprites.update()

    for sprite in self.visibile_sprites:
      pygame.draw.rect(self.display_surface, 'red', sprite.rect, 1)


