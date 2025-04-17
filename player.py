import pygame
from settings import *
from debug import debug
from support import import_folder_player
from entity import Entity
from support import fetch_weapon_data
from screens import DeathScreen


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_projectile, player_stats=DEFAULT_PLAYER_STATS):
        super().__init__(groups)
        original_image = pygame.image.load('graphics/player/down/down_0.png').convert_alpha()
        self.image = pygame.transform.scale(original_image, (PLAYERSIZE, PLAYERSIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -15)
        self.import_player_assets()

        # Armas
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.create_projectile = create_projectile
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200
        self.weapon_index = 0
        self.current_weapon = 'gun'
        
        # Inventário
        self.inventory = ['gun', 'axe', 'sword']

        # Orientação do jogador
        self.status = 'down'

        # Inicializar temporizadores de ataque
        self.attacking = False
        self.attacking_cool_down = 200
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        # Atributos do jogador
        self.player_stats = player_stats
        
        # Controle de munição
        self.ammo = 10  # Iniciar com 10 balas
        self.max_ammo = self.player_stats['max_ammo']  # Máximo de balas vindo das estatísticas do jogador
        self.no_ammo_message_timer = 0  # Timer para mensagem de sem munição
        
        # Sistema de moedas para a lojinha
        self.coins = 0  # Iniciar sem moedas
        self.thief_count = 0  # Contador de quantas vezes o jogador roubou da loja
    
        # Atributos de progressão
        self.level = 1
        self.health = self.player_stats['max_health']
        self.energy = 0  # Não usamos mais energia/mana
        self.speed = self.player_stats['speed']
        self.exp = 0
        self.super_counter = 0

        # damage timer
        self.vulnerable = True
        self.hit_time = None
        self.invulnerability_duration = 500
        
        # Fonte para mensagens
        self.font = pygame.font.Font(UI_FONT, 16)

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
            if animation == 'right':
                # Carregar e dividir a imagem especial para andar para a direita
                sprite_sheet = pygame.image.load('graphics/player/right_new/right.png').convert_alpha()
                frame_width = sprite_sheet.get_width() // 4
                frame_height = sprite_sheet.get_height()
                frames = []
                for i in range(4):
                    frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
                    frame = pygame.transform.scale(frame, (PLAYERSIZE, PLAYERSIZE))
                    frames.append(frame)
                self.animations['right'] = frames
            elif animation == 'left':
                # Carregar e dividir a imagem especial para andar para a esquerda
                sprite_sheet = pygame.image.load('graphics/player/right_new/left.png').convert_alpha()
                frame_width = sprite_sheet.get_width() // 4
                frame_height = sprite_sheet.get_height()
                frames = []
                for i in range(4):
                    frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
                    frame = pygame.transform.scale(frame, (PLAYERSIZE, PLAYERSIZE))
                    frames.append(frame)
                self.animations['left'] = frames
            elif animation == 'up':
                # Carregar e dividir a imagem especial para andar para cima
                sprite_sheet = pygame.image.load('graphics/player/right_new/up.png').convert_alpha()
                frame_width = sprite_sheet.get_width() // 4
                frame_height = sprite_sheet.get_height()
                frames = []
                for i in range(4):
                    frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
                    frame = pygame.transform.scale(frame, (PLAYERSIZE, PLAYERSIZE))
                    frames.append(frame)
                self.animations['up'] = frames
            elif animation == 'down':
                # Carregar e dividir a imagem especial para andar para baixo
                sprite_sheet = pygame.image.load('graphics/player/right_new/down.png').convert_alpha()
                frame_width = sprite_sheet.get_width() // 4
                frame_height = sprite_sheet.get_height()
                frames = []
                for i in range(4):
                    frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
                    frame = pygame.transform.scale(frame, (PLAYERSIZE, PLAYERSIZE))
                    frames.append(frame)
                self.animations['down'] = frames
            else:
                animation_folder_path = character_path + animation
                raw_frames = import_folder_player(animation_folder_path)
                scaled_frames = [
                    pygame.transform.scale(frame, (PLAYERSIZE, PLAYERSIZE)) for frame in raw_frames
                ]
                self.animations[animation] = scaled_frames



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
            if keys[pygame.K_LSHIFT] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                self.weapon_index += 1
                self.weapon_index = self.weapon_index % len(self.inventory)
                self.current_weapon = self.inventory[self.weapon_index]

            # A direção do jogador pode mudar quando ataca
            if keys[pygame.K_LEFT] and not self.attacking:
                self.status = 'left'
            elif keys[pygame.K_RIGHT] and not self.attacking:
                self.status = 'right'
            if keys[pygame.K_UP] and not self.attacking:
                self.status = 'up'
            elif keys[pygame.K_DOWN] and not self.attacking:
                self.status = 'down'

            # Se atacar, mudar para estado de ataque
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[
                pygame.K_DOWN] and not self.attacking:
                # Verificar se tem munição quando usar gun
                if self.current_weapon == 'gun':
                    if self.ammo > 0:  # Só permite atirar se tiver munição
                        self.attacking = True
                        self.attack_time = pygame.time.get_ticks()
                        self.create_attack(self.current_weapon)
                        self.ammo -= 1  # Diminui munição ao atirar
                    else:
                        # Feedback visual - ativar o timer da mensagem de sem munição
                        self.no_ammo_message_timer = 60  # Mostrar por 1 segundo (60 frames)
                else:  # Armas melee não usam munição
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    self.create_attack(self.current_weapon)

            # Ataque especial
            if keys[pygame.K_r]:
                if self.super_counter >= self.player_stats['super_threshold']:
                    self.super_counter = 0
                    self.health = min(self.player_stats['max_health'], self.health + 125)
            if keys[pygame.K_m]:
                if self.super_counter < self.player_stats['super_threshold']:
                    self.super_counter += 1

            # Recarregar munição
            if keys[pygame.K_SPACE]:
                self.ammo = self.max_ammo

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

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attacking_cool_down:
                self.attacking = False
                self.destroy_attack()

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invulnerability_duration:
                self.vulnerable = True

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        self.frame_index = self.frame_index % len(animation)

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_base_damage(self):
        # Calcular dano base reduzido com base em quantas vezes o jogador roubou
        # Cada roubo reduz o dano em 5% (multiplicativo)
        base_damage = self.player_stats['damage']
        if self.thief_count > 0:
            reduction_factor = 0.95 ** self.thief_count  # Redução de 5% por roubo
            base_damage = base_damage * reduction_factor
            
        return base_damage
        
    def add_coins(self, amount=1):
        """Adiciona moedas ao inventário do jogador"""
        self.coins += amount
        # Mostrar na tela quantas moedas o jogador ganhou
        if amount > 0:
            print(f"Ganhou {amount} moedas! Total: {self.coins}")
            
            # Mostrar mensagem visual na tela
            if hasattr(self, 'font'):
                self.coin_message_timer = 60  # Mostrar por 1 segundo
                self.coin_message_amount = amount
        
    def spend_coins(self, amount):
        """Gastar moedas na loja, retorna True se a transação foi bem-sucedida"""
        if self.coins >= amount:
            self.coins -= amount
            return True
        return False
        
    def steal_from_shop(self):
        """Roubar da lojinha, mas perder Destreza de Combate"""
        self.thief_count += 1
        
        # Reduzir a velocidade do jogador em 5% por cada roubo (cumulativo)
        reduction_factor = 0.95 ** self.thief_count
        self.player_stats['speed'] *= reduction_factor
        self.speed = self.player_stats['speed']
        
        return True

    def check_death(self):
        if self.health <= 0:
            death_screen = DeathScreen(pygame.display.get_surface())
            should_reset_level = death_screen.run()
            
            if should_reset_level:
                # Apenas retornar True para indicar que o nível deve ser recriado
                return True
            
            # Caso não tenha escolhido reiniciar, apenas restaurar os atributos do jogador
            self.health = self.player_stats['max_health']
            self.ammo = self.max_ammo
            self.exp = 0
            self.super_counter = 0
            
        return False  # Não é necessário recriar o nível

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.check_death()
        
        # Atualizar timer da mensagem de sem munição
        if self.no_ammo_message_timer > 0:
            self.no_ammo_message_timer -= 1
            
            # Exibir mensagem de sem munição
            if self.no_ammo_message_timer > 0:
                # Obter superfície atual
                screen = pygame.display.get_surface()
                
                # Criar mensagem de sem municao
                message = self.font.render("SEM MUNICAO!", True, (255, 0, 0))
                message_rect = message.get_rect(center=(screen.get_width() // 2, 100))
                
                # Desenhar fundo semi-transparente para a mensagem
                bg_surf = pygame.Surface((message_rect.width + 20, message_rect.height + 10))
                bg_surf.fill((50, 0, 0))
                bg_surf.set_alpha(180)
                bg_rect = bg_surf.get_rect(center=message_rect.center)
                
                # Desenhar na tela
                screen.blit(bg_surf, bg_rect)
                screen.blit(message, message_rect)
        
        # Mostrar mensagem de moedas ganhas, se necessário
        if hasattr(self, 'coin_message_timer') and self.coin_message_timer > 0:
            self.coin_message_timer -= 1
            
            if self.coin_message_timer > 0:
                # Obter superfície atual
                screen = pygame.display.get_surface()
                
                # Criar mensagem de moedas ganhas
                message = self.font.render(f"+{self.coin_message_amount} MOEDAS!", True, (255, 215, 0))
                message_rect = message.get_rect(center=(screen.get_width() // 2, 130))
                
                # Desenhar fundo semi-transparente para a mensagem
                bg_surf = pygame.Surface((message_rect.width + 20, message_rect.height + 10))
                bg_surf.fill((30, 30, 0))
                bg_surf.set_alpha(180)
                bg_rect = bg_surf.get_rect(center=message_rect.center)
                
                # Desenhar na tela
                screen.blit(bg_surf, bg_rect)
                screen.blit(message, message_rect)
