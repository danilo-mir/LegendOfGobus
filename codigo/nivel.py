import pygame
from settings import *
from quadrado import *
from jogador import *
from debug import *

class Nivel:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        for index_linha, linha in enumerate(WORLD_MAP):
            for index_col, col in enumerate(linha):
                x=index_col*TAMANHO_QUADRADO
                y=index_linha*TAMANHO_QUADRADO
                if col == 'x':
                    Quadrado((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Jogador((x, y), [self.visible_sprites])
    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        debug(self.player.direction)
