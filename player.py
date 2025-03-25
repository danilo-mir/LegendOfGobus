import pygame
import random
from settings import *
from debug import debug
from utils import import_folder

class Player(pygame.sprite.Sprite):
  def __init__(self, pos, groups, obstacle_sprites, visible_sprites, enemy_sprites):
    super().__init__(groups)
    self.image = pygame.image.load('graphics/player/down/down_0.png').convert_alpha()
    self.rect = self.image.get_rect(topleft = pos)
    self.hitbox = self.rect.inflate(0, -26)

    # Atributos usados para animação do movimento
    self.import_player_assets()
    self.status = 'down'
    self.frame_index = 0
    self.animation_speed = 0.15

    # Movimento
    self.direction = pygame.math.Vector2(0, 0)
    self.speed = 5
    self.attacking = False
    self.attacking_cool_down = 400
    self.attack_time = None

    self.obstacle_sprites = obstacle_sprites

    self.visible_sprites = visible_sprites
    self.enemy_sprites = enemy_sprites

    # Sistema de armas
    self.weapons = {
        'sword': {'damage': 10, 'cooldown': 400, 'range': 50},
        'bow': {'damage': 8, 'cooldown': 600, 'range': 200, 'ammo': 10},
        'fire_spell': {'damage': 15, 'cooldown': 800, 'effect': 'burn'}
    }
    self.current_weapon = 'sword'
    self.inventory = {
        'weapons': ['sword'],  # Armas disponíveis
        'items': {'potions': 3, 'arrows': 10}
    }

    def create_projectile(self):
      if self.current_weapon == 'bow':
          Projectile(
              pos=self.rect.center,
              direction=self.direction,
              groups=[self.visible_sprites],
              damage=self.weapons['bow']['damage'],
              speed=10,
              range=self.weapons['bow']['range'],
              image_path='graphics/weapons/arrow.png'
          )
    
    # Atributos de progressão
    self.level = 1
    self.exp = 0
    self.exp_to_level = 100
    self.max_health = 100
    self.health = self.max_health
    self.combat_dexterity = 100  # DC (Destreza de Combate)

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
      if keys[pygame.K_LEFT]:
        self.direction.x = -1
        self.status = 'left'
      elif keys[pygame.K_RIGHT]:
        self.direction.x = 1
        self.status = 'right'
      else:
        self.direction.x = 0
      
      if keys[pygame.K_UP]:
        self.direction.y = -1
        self.status = 'up'
      elif keys[pygame.K_DOWN]:
        self.direction.y = 1
        self.status = 'down'
      else:
        self.direction.y = 0

      # Input de ataque
      if keys[pygame.K_SPACE] and not self.attacking:
        self.attacking = True
        self.attack_time = pygame.time.get_ticks()
        debug('Ataque')

      # Input de magica
      if keys[pygame.K_LCTRL] and not self.attacking:
        self.attacking = True
        self.attack_time = pygame.time.get_ticks()
        debug('Magica')
      
      # Normalizar vetor velocidade para que andar na diagonal não seja mais rápido
      if self.direction.magnitude() > 0.1:
        self.direction = self.direction.normalize()

  def get_status(self):
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

  def animate(self):
    animation = self.animations[self.status]

    self.frame_index += self.animation_speed 
    self.frame_index = self.frame_index % len(animation)

    self.image = animation[int(self.frame_index)]
    self.rect = self.image.get_rect(center = self.hitbox.center)

  def update(self):
    self.input()
    self.cooldowns()
    self.get_status()
    self.animate()
    self.move(self.speed)

  #Sistema de Combate
  def attack(self):
      if not self.attacking:
          self.attacking = True
          self.attack_time = pygame.time.get_ticks()

          weapon = self.weapons[self.current_weapon]

          if self.current_weapon == 'bow' and self.inventory['items']['arrows'] > 0:
              self.inventory['items']['arrows'] -= 1
              self.create_projectile()
          elif self.current_weapon == 'bow' and self.inventory['items']['arrows'] <= 0:
              debug('Sem flechas!')
              self.attacking = False
              return

          debug(f'Ataque com {self.current_weapon} - Dano: {weapon["damage"]}')

          # Verifica colisão com inimigos
          for enemy in self.enemy_sprites:
              if self.check_attack_hit(enemy):
                  enemy.take_damage(weapon['damage'])
                  if 'effect' in weapon:
                      enemy.apply_effect(weapon['effect'])

  def create_projectile(self):
      # Cria uma flecha ou projétil mágico
      if self.current_weapon == 'bow':
          Projectile(
              pos=self.rect.center,
              direction=self.direction,
              groups=self.visible_sprites,
              damage=self.weapons['bow']['damage'],
              speed=10,
              range=self.weapons['bow']['range'],
              image_path='graphics/weapons/arrow.png'
          )

  #Checka colisão
  def check_collisions(self):
    # Colisão com inimigos
    for sprite in self.enemy_sprites:
        if sprite.hitbox.colliderect(self.rect):
            sprite.take_damage(self.damage)
            self.kill()
            return
    
    # Colisão com obstáculos
    for sprite in self.obstacle_sprites:
        if sprite.hitbox.colliderect(self.rect):
            self.kill()
            return
        
  def update(self):
      # Movimenta o projétil
      self.pos += self.direction * self.speed
      self.rect.center = self.pos

      # Verifica colisões
      self.check_collisions()

      # Calcula distância percorrida
      self.distance_traveled = self.start_pos.distance_to(self.pos)

      # Destrói o projétil se ultrapassar o alcance máximo
      if self.distance_traveled > self.range:
          self.kill()

  #Progressão de Hbailidade
  def gain_exp(self, amount):
      self.exp += amount
      if self.exp >= self.exp_to_level:
          self.level_up()

  def level_up(self):
      self.level += 1
      self.exp -= self.exp_to_level
      self.exp_to_level = int(self.exp_to_level * 1.5)

      # Melhorias por nível
      self.max_health += 10
      self.health = self.max_health
      self.speed += 0.2

      debug(f'Level Up! Novo nível: {self.level}')

  def upgrade_skill(self, skill):
      if skill == 'health':
          self.max_health += 20
      elif skill == 'speed':
          self.speed += 0.5
      elif skill == 'inventory':
          # Implementar aumento de capacidade do inventário
          pass
      
  #Interação com Lojas e NPCs
  def interact_with_shop(self, shop):
      # Lógica para comprar itens
      if shop.has_item('potion') and self.inventory['coins'] >= 50:
          self.inventory['potions'] += 1
          self.inventory['coins'] -= 50
      elif shop.has_item('arrows') and self.inventory['coins'] >= 10:
          self.inventory['arrows'] += 5
          self.inventory['coins'] -= 10
  
  def steal_from_shop(self, shop):
      """
      Tenta roubar um item da loja com 30% de chance de sucesso.
      Em caso de falha, reduz a Destreza de Combate (DC).
      """
      if not hasattr(self, 'combat_dexterity'):
          self.combat_dexterity = 100  # Valor padrão se não estiver definido

      success = random.random() < 0.3  # 30% de chance de sucesso

      if success:
          stolen_item = shop.get_random_item()
          if stolen_item:
              # Adiciona o item ao inventário
              if stolen_item in self.inventory['items']:
                  self.inventory['items'][stolen_item] += 1
              else:
                  self.inventory['items'][stolen_item] = 1
              debug(f'Item roubado: {stolen_item}')
          else:
              debug('A loja está vazia!')
      else:
          # Penalidade por falha no roubo
          penalty = random.randint(5, 15)  # Valor aleatório entre 5 e 15
          self.combat_dexterity = max(0, self.combat_dexterity - penalty)
          debug(f'Roubo falhou! -{penalty} DC (Total: {self.combat_dexterity})')

          # Verifica se os Druidas devem atacar
          if self.combat_dexterity <= 30:
              self.trigger_druid_attack()
  
  #Estado de efeito
  def apply_effect(self, effect):
      if effect == 'burn':
          self.burning = True
          self.burn_duration = 3000  # 3 segundos
          self.burn_damage = 2
          self.burn_time = pygame.time.get_ticks()
      elif effect == 'freeze':
          self.frozen = True
          self.freeze_duration = 2000  # 2 segundos
          self.freeze_time = pygame.time.get_ticks()
          self.speed /= 2  # Reduz velocidade pela metade
  
  def update_effects(self):
      current_time = pygame.time.get_ticks()
      
      if hasattr(self, 'burning') and self.burning:
          if current_time - self.burn_time >= 1000:  # Dano a cada segundo
              self.health -= self.burn_damage
              self.burn_time = current_time
          
          if current_time - self.burn_time >= self.burn_duration:
              self.burning = False
      
      if hasattr(self, 'frozen') and self.frozen:
          if current_time - self.freeze_time >= self.freeze_duration:
              self.frozen = False
              self.speed *= 2  # Restaura velocidade

  #Métodos adicionais
  def switch_weapon(self):
      # Alterna entre armas disponíveis
      available_weapons = self.inventory['weapons']
      current_index = available_weapons.index(self.current_weapon)
      next_index = (current_index + 1) % len(available_weapons)
      self.current_weapon = available_weapons[next_index]
      debug(f'Arma equipada: {self.current_weapon}')
  
  def use_potion(self):
      if self.inventory['items']['potions'] > 0:
          self.inventory['items']['potions'] -= 1
          self.health = min(self.health + 30, self.max_health)
          debug('Poção usada! +30 HP')
  
  def trigger_druid_attack(self):
      # Implementar ataque dos Druidas da Ordem Oculta (DOO)
      debug('Os Druidas da Ordem Oculta estão atacando!')
      # Adicionar inimigos DOO ao grupo de sprites

  #Atualização de update
  def update(self):
      self.input()
      self.cooldowns()
      self.get_status()
      self.animate()
      self.move(self.speed)
      self.update_effects()
      
      # Verifica se o jogador morreu
      if self.health <= 0:
          self.die()
  
  def die(self):
      debug('Game Over!')
      # Implementar lógica de morte e reinício

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, damage, speed, range, image_path):
        super().__init__(groups)
        
        # Configuração da imagem
        self.image = pygame.image.load(image_path).convert_alpha()
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

class Shop:
    def __init__(self):
        self.items = {
            'potion': {'price': 50, 'quantity': 10},
            'arrow': {'price': 10, 'quantity': 20},
            'fire_scroll': {'price': 100, 'quantity': 5}
        }
    
    def get_random_item(self):
        available_items = [item for item, details in self.items.items() if details['quantity'] > 0]
        if not available_items:
            return None
        return random.choice(available_items)