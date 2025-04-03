import pygame
from abc import ABC, abstractmethod
import json

class Weapon(ABC, pygame.sprite.Sprite):
  def __init__(self, weapon_name, player, groups):
    super().__init__(groups)

    # Achar a direção da arma com base na direção do jogador
    direction = player.status

    # Carregar sprite da arma
    self.full_path = f'graphics/weapons/{weapon_name}/{direction}.png'
    self.image = pygame.image.load(self.full_path)

    # Posicionar a arma corretamente para ficar na mão do jogador
    if direction == 'right':
       self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 16))
    elif direction == 'left':
       self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 16))
    elif direction == 'down':
       self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
    else:
       self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))

    self.hitbox = self.rect

  @abstractmethod
  def shoot():
    pass

class MeleeWeapon(Weapon):
  def __init__(self, weapon_name, player, groups):
     super().__init__(weapon_name, player, groups)

  def shoot():
     pass

class RangedWeapon(Weapon):
  pass

class Spell(Weapon):
  pass

# Converter tipo da arma para nome da classe
get_child_class = {
  'melee': MeleeWeapon,
  'ranged': RangedWeapon,
  'spell': Spell
}

# Fábrica de armas pois precisamos do nome da arma para saber a que tipo pertence
def create_weapon(weapon_name, player, groups):
  with open('weapons.json') as weapon_data_json:
    weapon_data = json.load(weapon_data_json)
  weapon_type = weapon_data[weapon_name]['type']
  weapon_child_class = get_child_class[weapon_type]
  return weapon_child_class(weapon_name, player, groups)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, damage, speed, range):
        super().__init__(groups)
        self.image = pygame.image.load("").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        
        # Propriedades do projétil
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.range = range
        
        # Controle de distância
        self.start_pos = pygame.math.Vector2(pos)
        self.distance_traveled = 0
        
        # Rotaciona a imagem conforme a direção
        if direction.x > 0:  # Direita
            self.image = pygame.transform.rotate(self.image, -90)
        elif direction.x < 0:  # Esquerda
            self.image = pygame.transform.rotate(self.image, 90)
        elif direction.y > 0:  # Baixo
            pass  # Imagem padrão já aponta para baixo
        elif direction.y < 0:  # Cima
            self.image = pygame.transform.rotate(self.image, 180)
    
    def update(self):
        # Movimenta o projétil
        self.pos += self.direction * self.speed
        self.rect.center = self.pos
        
        # Calcula distância percorrida
        self.distance_traveled = self.start_pos.distance_to(self.pos)
        
        # Destrói o projétil se ultrapassar o alcance máximo
        if self.distance_traveled > self.range:
           self.kill()