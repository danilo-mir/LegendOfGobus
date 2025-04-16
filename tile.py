import pygame
from settings import *

class BaseTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, image_path, size):
        super().__init__(groups)
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, size)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15, -10)
