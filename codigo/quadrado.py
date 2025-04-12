import pygame
from settings import*

class Quadrado(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/rock_20.png').convert_alpha()
        #posicoes de objetos graficos para fazer as colisoes
        self.rect = self.image.get_rect(topleft = (pos[0]+6, pos[1]+6))

"""
class Quadrado(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((0, 0))  # Surface with no visible size
        self.rect = pygame.Rect(pos[0], pos[1], 50, 50)  # Define a rect for collisions
"""