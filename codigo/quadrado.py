import pygame
from settings import*

class Quadrado(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/rock.png').convert_alpha()
        #posicoes de objetos graficos para fazer as colisoes
        self.rect = self.image.get_rect(topleft = pos)