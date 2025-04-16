import pygame
from settings import *

class BaseTile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, image_path, size):
        super().__init__(groups)
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, size)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-15, -10)

class Grass1Tile(BaseTile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 'graphics/grass/grass_1.png', (GRASSSIZE, GRASSSIZE))

class Grass2Tile(BaseTile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 'graphics/grass/grass_2.png', (GRASSSIZE, GRASSSIZE))

class Grass3Tile(BaseTile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 'graphics/grass/grass_3.png', (GRASSSIZE, GRASSSIZE))

class Trunk1Tile(BaseTile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 'graphics/objects/0.png', (TILESIZE, TILESIZE))

class Trunk2Tile(BaseTile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 'graphics/objects/01.png', (TILESIZE, TILESIZE))

class Tree1Tile(BaseTile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 'graphics/objects/02.png', (TILESIZE, TILESIZE))

class Tree2Tile(BaseTile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 'graphics/objects/03.png', (TILESIZE, TILESIZE))

class Tree3Tile(BaseTile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 'graphics/objects/04.png', (TILESIZE, TILESIZE))

class Rock1Tile(BaseTile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 'graphics/objects/08.png', (TILESIZE, TILESIZE))

class DetailsTile(BaseTile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 'graphics/tilemap/details.png', (TILESIZE, TILESIZE))

# Novos tiles para a fase de gelo
class IceTree1Tile(BaseTile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 'graphics/objects/05.png', (TILESIZE, TILESIZE))

class IceTree2Tile(BaseTile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 'graphics/objects/06.png', (TILESIZE, TILESIZE))

class IceTree3Tile(BaseTile):
    def __init__(self, pos, groups):
        super().__init__(pos, groups, 'graphics/objects/07.png', (TILESIZE, TILESIZE))