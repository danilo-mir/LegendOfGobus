import pygame
from abc import ABC, abstractmethod
from support import fetch_weapon_data
from entity import Entity


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

        # --- NEW CODE START (Weapon Image Scaling - Optional for weapons themselves) ---
        # Define the desired scale factor for the weapon image
        weapon_scale_factor = 0.7
        new_weapon_size = (int(original_image.get_width() * weapon_scale_factor),
                           int(original_image.get_height() * weapon_scale_factor))
        self.image = pygame.transform.scale(original_image, new_weapon_size)
        # --- NEW CODE END ---

        # Posicionar a arma corretamente para ficar na mão do jogador
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(weapon_data["r_horizontal_offset"], weapon_data['lr_vertical_offset']))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(weapon_data["l_horizontal_offset"], weapon_data['lr_vertical_offset']))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(weapon_data['ud_horizontal_offset'], weapon_data['d_vertical_offset']))
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(weapon_data['ud_horizontal_offset'], weapon_data['u_vertical_offset']))

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


class Projectile(Entity):
    def __init__(self, projectile_data, player, groups, obstacle_sprites):
        super().__init__(groups)

        self.speed = projectile_data['speed']
        self.damage = projectile_data['damage'] + player.player_stats['damage']

        self.obstacle_sprites = obstacle_sprites

        direction = player.status

        self.full_path = f'{projectile_data["graphic"]}/{direction}.png'
        original_image = pygame.image.load(self.full_path).convert_alpha()

        # --- NEW CODE START (Projectile Image Scaling) ---
        # Define the desired scale factor for the projectile
        self.scale_factor = 0.7  # You can set a default here or make it configurable
        new_size = (int(original_image.get_width() * self.scale_factor),
                    int(original_image.get_height() * self.scale_factor))
        self.image = pygame.transform.scale(original_image, new_size)
        # --- NEW CODE END ---

        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(projectile_data["r_horizontal_offset"], projectile_data['lr_vertical_offset']) * self.scale_factor)
            self.direction = pygame.Vector2(1, 0)
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(projectile_data["l_horizontal_offset"], projectile_data['lr_vertical_offset']) * self.scale_factor)
            self.direction = pygame.Vector2(-1, 0)
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(projectile_data['ud_horizontal_offset'] * self.scale_factor, projectile_data['d_vertical_offset']))
            self.direction = pygame.Vector2(0, 1)
        else:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(projectile_data['ud_horizontal_offset'] * self.scale_factor, projectile_data['u_vertical_offset']))
            self.direction = pygame.Vector2(0, -1)
        self.hitbox = self.rect

    def set_scale(self, scale):
        """Allows you to change the scale of the projectile after initialization."""
        if scale > 0:
            self.scale_factor = scale
            original_image = pygame.image.load(self.full_path).convert_alpha()
            new_size = (int(original_image.get_width() * self.scale_factor),
                        int(original_image.get_height() * self.scale_factor))
            self.image = pygame.transform.scale(original_image, new_size)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.hitbox = self.rect

    def get_damage(self):
        return self.damage
    
    def collision(self, direction):
      "Check for collision and remove the object if it occurs"
      collided = super().collision(direction)
      if collided:
        self.kill()  # A bala desaparece se colidir com algum obstáculo
      return collided

    def update(self):
        self.move(self.speed)


# Converter tipo da arma para nome da classe
get_child_class = {
    'melee': MeleeWeapon,
    'ranged': RangedWeapon
}


# Fábrica de armas pois precisamos do nome da arma para saber a que tipo pertence
def create_weapon(weapon_name, player, groups):
    all_weapons_data = fetch_weapon_data()
    weapon_data = all_weapons_data[weapon_name]
    weapon_child_class = get_child_class[weapon_data['type']]
    return weapon_child_class(weapon_data, player, groups)