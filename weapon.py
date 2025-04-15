import pygame
from abc import ABC, abstractmethod
from support import fetch_weapon_data


class Weapon(ABC, pygame.sprite.Sprite):
    def __init__(self, weapon_data, player, groups):
        super().__init__(groups)
        
        # The damage done by the weapon
        self.damage = weapon_data['damage'] + player.player_stats['damage']

        # Achar a direção da arma com base na direção do jogador
        direction = player.status

        # Carregar sprite da arma
        self.full_path = f'{weapon_data["graphic"]}/{direction}.png'
        original_image = pygame.image.load(self.full_path).convert_alpha()  # Use convert_alpha for transparency

        # --- NEW CODE START ---
        # Define the desired scale factor (e.g., 2 for doubling the size)
        scale_factor = 0.7
        new_size = (int(original_image.get_width() * scale_factor),
                    int(original_image.get_height() * scale_factor))
        self.image = pygame.transform.scale(original_image, new_size)
        # --- NEW CODE END ---

        # Posicionar a arma corretamente para ficar na mão do jogador
        if direction == 'right':
          self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, weapon_data['horizontal_offset']))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, weapon_data['horizontal_offset']))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(weapon_data['vertical_offset'], 0))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(weapon_data['vertical_offset'], 0))

        self.hitbox = self.rect

    def get_damage(self):
      return self.damage


class MeleeWeapon(Weapon):
  def __init__(self, weapon_data, player, groups):
    super().__init__(weapon_data, player, groups)



class RangedWeapon(Weapon):
  def __init__(self, weapon_data, player, groups):
    super().__init__(weapon_data, player, groups)
    projectile_data = weapon_data['projectile']
    player.create_projectile(projectile_data)
    

class Projectile(pygame.sprite.Sprite):
  def __init__(self, projectile_data, player, groups):
    super().__init__(groups)

    self.speed = projectile_data['speed']
    self.damage = projectile_data['damage'] + player.player_stats['damage']
    
    direction = player.status

    self.full_path = f'{projectile_data["graphic"]}/{direction}.png'
    self.image = pygame.image.load(self.full_path)
    
    if direction == 'right':
      self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, projectile_data['horizontal_offset']))
      self.direction = pygame.Vector2(1, 0)
    elif direction == 'left':
      self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, projectile_data['horizontal_offset']))
      self.direction = pygame.Vector2(-1, 0)
    elif direction == 'down':
       self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(projectile_data['vertical_offset'], 0))
       self.direction = pygame.Vector2(0, 1)
    else:
       self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(projectile_data['vertical_offset'], 0))
       self.direction = pygame.Vector2(0, -1)
    self.hitbox = self.rect


  def get_damage(self):
     return self.damage
  
  def update(self):
    self.hitbox.x += self.direction.x * self.speed
    self.hitbox.y += self.direction.y * self.speed
    self.rect.center = self.hitbox.center



# Converter tipo da arma para nome da classe
get_child_class = {
  'melee' : MeleeWeapon,
  'ranged' : RangedWeapon
}


# Fábrica de armas pois precisamos do nome da arma para saber a que tipo pertence
def create_weapon(weapon_name, player, groups):
    all_weapons_data = fetch_weapon_data()
    weapon_data = all_weapons_data[weapon_name]
    weapon_child_class = get_child_class[weapon_data['type']]
    return weapon_child_class(weapon_data, player, groups)