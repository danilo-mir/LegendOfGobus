import pygame
from settings import *
from tile import *
from player import Player
from enemy import Enemy
from debug import debug
from ui import UI
from weapon import create_weapon, Projectile
from support import fetch_weapon_data
from wind import WindSystem  # Importar o sistema de vento


class Level:
    def __init__(self, game_map=WORLD_MAP, background=FORESTBG):
        # Acesso à variável da tela
        self.display_surface = pygame.display.get_surface()
        self.game_map = game_map
        self.background = background
        
        # Verificar se estamos na fase do deserto
        self.is_desert = background == 'graphics/tilemap/desertground.png'
        
        # Sistema de vento (apenas no deserto)
        self.wind_system = WindSystem(self.display_surface) if self.is_desert else None
        
        # Criar grupos de sprites
        self.visibile_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        # Sprites de ataque
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        # Criar mapa
        self.create_map()
        # Interface do usuário
        self.ui = UI()

    def create_map(self):
        for row_index, row in enumerate(self.game_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'G1':
                    Grass1Tile((x, y), [self.visibile_sprites, self.obstacle_sprites])
                if col == 'G2':
                    Grass2Tile((x, y), [self.visibile_sprites, self.obstacle_sprites])
                if col == 'G3':
                    Grass3Tile((x, y), [self.visibile_sprites, self.obstacle_sprites])
                if col == 'TR1':
                    Trunk1Tile((x, y), [self.visibile_sprites, self.obstacle_sprites])
                if col == 'TR2':
                    Trunk2Tile((x, y), [self.visibile_sprites, self.obstacle_sprites])
                if col == 'T1':
                    Tree1Tile((x, y), [self.visibile_sprites, self.obstacle_sprites])
                if col == 'T2':
                    Tree2Tile((x, y), [self.visibile_sprites, self.obstacle_sprites])
                if col == 'T3':
                    Tree3Tile((x, y), [self.visibile_sprites, self.obstacle_sprites])
                if col == 'R1':
                    Rock1Tile((x, y), [self.visibile_sprites, self.obstacle_sprites])
                if col == 'P':
                    self.player = Player(
                        (x, y),
                        [self.visibile_sprites],
                        self.obstacle_sprites,
                        self.create_attack,
                        self.destroy_attack,
                        self.create_projectile)
                elif col in monster_symbol:
                    monster_name = monster_symbol[col]
                    Enemy(
                        monster_name,
                        (x, y),
                        [self.visibile_sprites, self.attackable_sprites],
                        self.obstacle_sprites,
                        self.damage_player
                    )

    def create_attack(self, weapon_name):
        weapon_type = fetch_weapon_data()[weapon_name]['type']
        groups = [self.visibile_sprites, self.attack_sprites] if weapon_type == 'melee' else [self.visibile_sprites]
        self.current_attack = create_weapon(weapon_name, self.player, groups)

    def create_projectile(self, projectile_data):
        Projectile(projectile_data, self.player, [self.visibile_sprites, self.attack_sprites], self.obstacle_sprites)
    
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    
    def change_visibility(self, sprite, visible):
        if visible:
            if sprite not in self.visibile_sprites:
                self.visibile_sprites.add(sprite)
        else:
            if sprite in self.visibile_sprites:
                self.visibile_sprites.remove(sprite)

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        weapon_damage = attack_sprite.get_damage()
                        target_sprite.get_damage(self.player, weapon_damage)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hit_time = pygame.time.get_ticks()

    def run(self):
        self.display_surface.blit(pygame.transform.scale(pygame.image.load(self.background).convert_alpha(), (WIDTH, HEIGHT)), (0, 0))  # Draw background image
        
        # Atualizar e aplicar o sistema de vento ao jogador se estiver no deserto
        if self.is_desert and self.wind_system:
            self.wind_system.update()
            
            # Aplicar o efeito do vento no jogador
            wind_dir, wind_strength = self.wind_system.get_player_speed_modifier()
            
            # Calcular o produto escalar entre a direção do jogador e a direção do vento
            # Valores positivos indicam que o jogador está se movendo a favor do vento
            # Valores negativos indicam que o jogador está se movendo contra o vento
            player_dir = self.player.direction.normalize() if self.player.direction.magnitude() > 0 else pygame.Vector2(0, 0)
            dot_product = player_dir.dot(wind_dir) if wind_dir.magnitude() > 0 else 0
            
            # Ajustar a velocidade do jogador
            speed_modifier = 1.0
            if dot_product > 0.3:  # Jogador a favor do vento
                speed_modifier = 1.0 + (wind_strength * 0.5)  # Aumento de até 50% na velocidade
            elif dot_product < -0.3:  # Jogador contra o vento
                speed_modifier = 1.0 - (wind_strength * 0.6)  # Redução de até 60% na velocidade
            
            # Aplicar o modificador de velocidade
            self.player.speed = self.player.player_stats['speed'] * speed_modifier
            
            # Desenhar as partículas do vento
            self.wind_system.draw()
        else:
            # Restaurar a velocidade normal quando não está no deserto
            self.player.speed = self.player.player_stats['speed']
        
        self.visibile_sprites.custom_draw(self.player)
        self.visibile_sprites.update()
        self.visibile_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
        debug(self.attack_sprites)
        
        # Mostrar informações do vento quando estiver no deserto
        if self.is_desert and self.wind_system:
            wind_dir, wind_strength = self.wind_system.get_player_speed_modifier()
            wind_info = f"Vento: {wind_dir.x:.1f},{wind_dir.y:.1f} | Força: {wind_strength:.1f}"
            debug(wind_info, 40)  # Adiciona informações do vento abaixo das outras infos
        
        # Verificar se o jogador morreu e o nível deve ser recriado
        # Este valor será utilizado pela classe Game
        self.should_reset_level = False
        if hasattr(self.player, 'check_death'):
            self.should_reset_level = self.player.check_death()
        
        return self.should_reset_level


# Grupo de sprites customizado para ordena-los conforme sua posicao y dando um senso de profundidade
# Também implementa o movimento da câmera caso o mapa seja maior que a tela
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

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos_rect = sprite.rect.topleft - self.offset
            offset_pos_hitbox = sprite.hitbox.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos_rect)
            drawn_rect = pygame.Rect(offset_pos_rect[0], offset_pos_rect[1], sprite.rect.width, sprite.rect.height)
            drawn_hitbox = pygame.Rect(offset_pos_hitbox[0], offset_pos_hitbox[1], sprite.hitbox.width, sprite.hitbox.height)
            pygame.draw.rect(self.display_surface, 'red', drawn_rect, 1)
            pygame.draw.rect(self.display_surface, 'green', drawn_hitbox, 1)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)