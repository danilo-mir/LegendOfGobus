import pygame
from settings import *
from tile import *
from player import Player
from enemy import Enemy
from debug import debug
from ui import UI
from weapon import create_weapon


class Level:
    def __init__(self):
        # Acesso à variável da tela
        self.display_surface = pygame.display.get_surface()

        # Criar grupos de sprites
        self.visibile_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Sprites de ataque
        self.current_attack = None

        # Criar mapa
        self.create_map()

        # Interface do usuário
        self.ui = UI()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
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
                    self.player = Player((x, y), [self.visibile_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)
                elif col in monster_symbol:
                    monster_name = monster_symbol[col]
                    Enemy(monster_name, (x, y), [self.visibile_sprites], self.obstacle_sprites)

    def create_attack(self, weapon_name):
        self.current_attack = create_weapon(weapon_name, self.player, [self.visibile_sprites])  
    
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

    def run(self):
        self.display_surface.fill((0, 100, 0))
        self.visibile_sprites.custom_draw(self.player)
        self.visibile_sprites.update()
        self.visibile_sprites.enemy_update(self.player)
        self.ui.display(self.player)


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