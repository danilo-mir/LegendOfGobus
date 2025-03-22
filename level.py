import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
  def __init__(self):
    # Acesso à variável da tela
    self.display_surface = pygame.display.get_surface()
    
    # Criar grupos de sprites
    self.visibile_sprites = YSortCameraGroup()
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
          self.player = Player((x, y), [self.visibile_sprites], self.obstacle_sprites)


  def run(self):
    self.visibile_sprites.custom_draw(self.player)
    self.visibile_sprites.update()

# Grupo de sprites customizado para ordena-los conforme sua posicao y dando um senso de profundidade
class YSortCameraGroup(pygame.sprite.Group):
  def __init__(self):
    super().__init__()
    self.display_surface = pygame.display.get_surface()
    self.half_width = self.display_surface.get_size()[0] // 2
    self.half_height = self.display_surface.get_size()[1] // 2
    self.offset = pygame.math.Vector2()

  def custom_draw(self, player):
    self.offset.x = 0
    self.offset.y = 0
  
    # Descomentar se a camera for mover ao longo dos niveis

    # self.offset.x = player.rect.centerx - self.half_width
    # self.offset.y = player.rect.centery - self.half_height

    for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
      offset_pos_rect = sprite.rect.topleft - self.offset
      offset_pos_hitbox = sprite.hitbox.topleft - self.offset
      self.display_surface.blit(sprite.image, offset_pos_rect)
      drawn_rect = pygame.Rect(offset_pos_rect[0], offset_pos_rect[1], sprite.rect.width, sprite.rect.height)
      drawn_hitbox = pygame.Rect(offset_pos_hitbox[0], offset_pos_hitbox[1], sprite.hitbox.width, sprite.hitbox.height)
      pygame.draw.rect(self.display_surface, 'red', drawn_rect, 1)
      pygame.draw.rect(self.display_surface, 'green', drawn_hitbox, 1)
  
      


