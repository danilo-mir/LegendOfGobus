import pygame


class Entity(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        return True
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        return True

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.hitbox.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        return True
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        return True
        return False

    def get_status(self, *args):
        raise NotImplementedError("Subclassses must implement this method")