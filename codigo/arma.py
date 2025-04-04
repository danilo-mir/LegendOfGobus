import pygame

class Arma(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.status.split('_')
        print(direction)
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=player.rect.center)