import math
from support import *
from settings import *
import pygame
from settings import *
from entity import Entity
from debug import *


class Enemy(Entity):
    def __init__(self, name, pos, groups, obstacle_sprites, damage_player):
        super().__init__(groups)
        self.sprite_type = "enemy"

        # graphics
        self.status = 'idle'
        self.animations = self.import_graphics(name)
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']

        # interaction with player
        self.damage_player = damage_player
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def import_graphics(self, name):
        animations = {
            'idle': [],
            'move': [],
            'attack': []
        }
        main_path = f"graphics/monsters/{name}/"
        for animation in animations.keys():
            animations[animation] = import_folder(main_path + animation)
        return animations

    def get_player_distance_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)

        distance = (player_vector - enemy_vector).magnitude()

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        tup = (distance, direction)
        return tup

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, weapon_damage):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            self.health -= player.get_base_damage() + weapon_damage
            self.player = player
        self.hit_time = pygame.time.get_ticks()
        self.vulnerable = False

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def check_death(self):
        if self.health <= 0:
            if hasattr(self, 'player') and self.player:
                self.player.add_coins(1)
            self.kill()

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
