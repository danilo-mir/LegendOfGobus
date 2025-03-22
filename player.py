import pygame
from settings import *
from debug import debug

class Player(pygame.sprite.Sprite):
  def __init__(self, pos, groups, obstacle_sprites):
    super().__init__(groups)
    self.image = pygame.image.load('graphics/player/down/down_0.png').convert_alpha()
    self.rect = self.image.get_rect(topleft = pos)
    self.hitbox = self.rect.inflate(0, -26)

    self.direction = pygame.math.Vector2(0, 0)
    self.speed = 5

    self.obstacle_sprites = obstacle_sprites

  def input(self): 
    keys = pygame.key.get_pressed()

    # Input de movimento
    if keys[pygame.K_LEFT]:
      self.direction.x = -1
    elif keys[pygame.K_RIGHT]:
      self.direction.x = 1
    else:
      self.direction.x = 0
    
    if keys[pygame.K_UP]:
      self.direction.y = -1
    elif keys[pygame.K_DOWN]:
      self.direction.y = 1
    else:
      self.direction.y = 0
    
    # Normalizar vetor velocidade para que a diagonal não seja mais rápida
    if self.direction.magnitude() > 0.1:
      self.direction = self.direction.normalize()

  def move(self, speed):
    self.hitbox.x += self.direction.x * speed
    # Corrigir colisões devido ao movimento horizontal
    self.collision('horizontal')
    self.hitbox.y += self.direction.y * speed
    # Corrigir colisões devido ao movimento vertical
    self.collision('vertical')
    self.rect.center = self.hitbox.center	

  def collision(self, direction):
    if direction == 'horizontal':
      for sprite in self.obstacle_sprites:
        if sprite.hitbox.colliderect(self.hitbox):
          if self.direction.x > 0:
            self.hitbox.right = sprite.hitbox.left
          if self.direction.x < 0:
            self.hitbox.left = sprite.hitbox.right

    if direction == 'vertical':
      for sprite in self.obstacle_sprites:
        if sprite.hitbox.colliderect(self.hitbox):
          if self.hitbox.y > 0:
            self.hitbox.bottom = sprite.hitbox.top
          if self.direction.y < 0:
            self.hitbox.top = sprite.hitbox.bottom

  def update(self):
    self.input()
    self.move(self.speed)
