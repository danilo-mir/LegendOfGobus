import pygame
from settings import *
from quadrado import *
from jogador import *
from debug import *
from arma import *
from enemy import Enemy

class Nivel:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()

        self.fase_jogo = 1
        self.clique_j = False
        self.tempo_clique = 0

        self.create_map()

    def create_map(self):
        self.visible_sprites.empty()
        self.obstacle_sprites.empty()

        if self.fase_jogo == 1:
            WORLD_MAP = WORLD_MAP_1
        elif self.fase_jogo == 2:
            WORLD_MAP = WORLD_MAP_2
        elif self.fase_jogo == 3:
            WORLD_MAP = WORLD_MAP_3
        elif self.fase_jogo == 4:
            WORLD_MAP = WORLD_MAP_4
        for index_linha, linha in enumerate(WORLD_MAP):
            for index_col, col in enumerate(linha):
                x=index_col*TAMANHO_QUADRADO
                y=index_linha*TAMANHO_QUADRADO
                if col == 'x':
                    Quadrado((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Jogador((x, y), [self.visible_sprites], self.obstacle_sprites, self.bullet_group)
                elif col in monster_symbol:
                     monster_name = monster_symbol[col]
                     Enemy(monster_name, (x, y), [self.visible_sprites], self.obstacle_sprites)
        
        if self.fase_jogo == 1:
            self.floor_surface = pygame.image.load("graphics/deepnight_map/floresta/floresta_sem_grid.png").convert()
        elif self.fase_jogo == 2:
            self.floor_surface = pygame.image.load("graphics/deepnight_map/gelo/gelo.png").convert()
        elif self.fase_jogo == 3:
            self.floor_surface = pygame.image.load("graphics/deepnight_map/vulcao/vulcao.png").convert()
        elif self.fase_jogo == 4:
            self.floor_surface = pygame.image.load("graphics/deepnight_map/deserto/deserto.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0,0))

        self.floor_offset_pos = self.floor_rect.topleft
        #self.player - Jogador((2000,1430),[self.visible_sprites], self.obstacle_sprites, self.create_ataque)

    def create_ataque(self):
        Arma(self.player, [self.visible_sprites])

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.visible_sprites if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
           enemy.enemy_update(player)

    def run(self):
        self.display_surface.blit(self.floor_surface, self.floor_offset_pos)

        self.visible_sprites.draw(self.display_surface)
        self.bullet_group.draw(self.display_surface)

        self.visible_sprites.update()
        self.enemy_update(self.player)
        self.bullet_group.update()

        #debug(self.player.direction)

        keys = pygame.key.get_pressed()    
        if keys[pygame.K_j]:
            self.clique_j=True
            self.verificar_delay_clique()
            if self.clique_j:
                self.tempo_clique = pygame.time.get_ticks()
                self.fase_jogo += 1
                self.create_map()
        
    def verificar_delay_clique(self):
        tempo_atual = pygame.time.get_ticks()

        if self.clique_j:
            if tempo_atual - self.tempo_clique <= 400:
                self.clique_j = False

        