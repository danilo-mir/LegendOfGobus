import pygame
import random
from settings import *
from debug import debug
from utils import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, player_stats=DEFAULT_PLAYER_STATS):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/player/down/down_0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.import_player_assets()

        # Dar ao jogador acesso à função create_attack da classe Level
        self.create_attack = create_attack

        # Dar ao jogador acesso à funçào destroy_weapon da classe Level
        self.destroy_attack = destroy_attack

        # Orientação do jogador
        self.status = 'down'

        # Atributos utilizados para animar o movimento do jogador
        self.frame_index = 0
        self.animation_speed = 0.15

        # Movimento
        self.direction = pygame.math.Vector2(0, 0)

        # Inicializar temporizadores de ataque
        self.attacking = False
        self.attacking_cool_down = 400
        self.attack_time = None

        # Referência para o vetor de obstáculos do nível
        self.obstacle_sprites = obstacle_sprites

        # Atributos do jogador
        self.player_stats = player_stats

        # Arma equipada e inventário
        self.inventory = {}
        self.current_weapon = 'axe'
    
        # Atributos de progressão
        self.level = 1
        self.health = self.player_stats['max_health']
        self.energy = self.player_stats['max_energy']
        self.speed = self.player_stats['speed']
        self.exp = 0
        self.super_counter = 0

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
        'up': [],
        'down': [],
        'left': [],
        'right': [],
        'up_idle': [],
        'down_idle': [],
        'left_idle': [],
        'right_idle': [],
        'up_attack': [],
        'down_attack': [],
        'left_attack': [],
        'right_attack': [],
        }

        for animation in self.animations.keys():
            animation_folder_path = character_path + animation
            self.animations[animation] = import_folder(animation_folder_path)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # Input de movimento
            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            # A direção do jogador pode mudar quando ataca
            if keys[pygame.K_LEFT] and not self.attacking:
                self.status = 'left'
                debug(self.status)
            elif keys[pygame.K_RIGHT] and not self.attacking:
                self.status = 'right'
            if keys[pygame.K_UP] and not self.attacking:
                self.status = 'up'
            elif keys[pygame.K_DOWN] and not self.attacking:
                self.status = 'down'

            # Se atacar, mudar para estado de ataque
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[
                pygame.K_DOWN] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack(self.current_weapon)

            # Ataque especial
            if keys[pygame.K_r]:
                if self.super_counter >= self.player_stats['super_threshold']:
                    self.super_counter = 0
            if keys[pygame.K_m]:
                if self.super_counter < self.player_stats['super_threshold']:
                    self.super_counter += 1

            # Normalizar vetor velocidade para que andar na diagonal não seja mais rápido
            if self.direction.magnitude() > 0.1:
                self.direction = self.direction.normalize()

    def get_status(self):
        # Aqui o sprite do jogador será atualizado para ser um sprite do tipo parado (_iddle) ou de ataque(_attack)

        # Estado parado
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not self.attacking:
                if 'attack' in self.status:
                    self.status = self.status.replace('_attack', '_idle')
                else:
                    self.status = self.status + '_idle'

        # Estado atacando
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'

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

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attacking_cool_down:
                self.attacking = False
                self.destroy_attack()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        self.frame_index = self.frame_index % len(animation)

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)


    # Sistema de Combate
    def attack(self):
        if not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()

            weapon = self.weapons[self.current_weapon]

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
