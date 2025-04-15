import pygame
from settings import*
from debug import *
from support import *

class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, bullet_group):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player_redimencionado.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.import_player_assets()

        self.direction = pygame.math.Vector2()
        self.speed = 2
        self.atacando = False
        self.tempo_delay_ataque = 400
        self.tempo_ataque = None

        self.obstacle_sprites = obstacle_sprites

        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        # Arma
        self.arma_visivel = False
        self.balas = 5
        self.bullet_group = bullet_group
        self.arma_imgs = {
            'up': pygame.transform.scale(pygame.image.load("graphics/weapons/gun/arma_up.png"), (20, 20)),
            'down': pygame.transform.scale(pygame.image.load("graphics/weapons/gun/arma_down.png"), (20, 20)),
            'left': pygame.transform.scale(pygame.image.load("graphics/weapons/gun/arma_left.png"), (20, 20)),
            'right': pygame.transform.scale(pygame.image.load("graphics/weapons/gun/arma_right.png"), (20, 20)),
        }
    
    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'up_parado': [],
            'down_parado': [],
            'left_parado': [],
            'right_parado': [],
            'up_atacando': [],
            'down_atacando': [],
            'left_atacando': [],
            'right_atacando': [],
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)



    def input(self):
        keys = pygame.key.get_pressed()

        #comandos de movimento
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y=-1
            self.status = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y=1
            self.status = "down"
        else:
            self.direction.y=0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x=1
            self.status = "right"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x=-1
            self.status = "left"
        else:
            self.direction.x=0

        #comando de ataque
        if keys[pygame.K_z] and not self.atacando:
            self.atacando = True
            #registra o tempo de ataque
            self.tempo_ataque = pygame.time.get_ticks()
            self.create_ataque()
        
        # alternar arma
        if keys[pygame.K_g]:
            self.arma_visivel = not self.arma_visivel
            pygame.time.wait(200)

        # tiro
        if keys[pygame.K_k] and self.arma_visivel and self.balas > 0:
            self.shoot()
            pygame.time.wait(150)

    def shoot(self):
        direction = pygame.math.Vector2(0, 0)
        if 'up' in self.status:
            direction = pygame.math.Vector2(0, -1)
        elif 'down' in self.status:
            direction = pygame.math.Vector2(0, 1)
        elif 'left' in self.status:
            direction = pygame.math.Vector2(-1, 0)
        elif 'right' in self.status:
            direction = pygame.math.Vector2(1, 0)

        bullet = Bala(self.rect.center, direction, self.obstacle_sprites, self.status)
        self.bullet_group.add(bullet)
        self.balas -= 1

    #usar move() para jogador e para inimigos
    #por isso n usar self.speed
    def move(self, speed):
        #corrigindo para q n corra mais rapido na diagonal
        if self.direction.magnitude() !=0:
            self.direction = self.direction.normalize()
        self.rect.center += self.direction *speed

        self.rect.x+=self.direction.x*speed
        self.colisao('horizontal')
        self.rect.y+=self.direction.y*speed
        self.colisao('vertical')

    def get_status(self):

        if self.direction.x == 0 and self.direction.y == 0:
            if not '_parado' in self.status and not 'atacando' in self.status:
                self.status = self.status + '_parado' 
                #passo a ter as informacoes de left e left_parado

        if self.atacando:
            self.direction.x = 0
            self.direction.y = 0
            if not '_atacando' in self.status:
                    if 'parado' in self.status:
                        self.status = self.status.replace('_parado', '_atacando')
                    else:
                        self.status = self.status + '_atacando'
            #assim n misturamos left_parado e left_atacando
        else:
            self.status = self.status.replace('_atacando', '')
            #troca left_atacando pra left quando para de atacar

    def colisao(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x>0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x<0:
                        self.rect.left = sprite.rect.right

        if direction =='vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y>0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y<0:
                        self.rect.top = sprite.rect.bottom
    
    def verificar_delay_ataque(self):
        tempo_atual = pygame.time.get_ticks()

        if self.atacando:
            if tempo_atual - self.tempo_ataque >= self.tempo_delay_ataque:
                self.atacando = False
            
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index = (self.frame_index + self.animation_speed) % len(animation)
        base_image = animation[int(self.frame_index)]
        if self.arma_visivel:
            self.image = base_image.copy()
            direcao_base = self.status.split('_')[0]
            if direcao_base in self.arma_imgs:
                arma = self.arma_imgs[direcao_base]
                self.image.blit(arma, (10, 20))
        else:
            self.image = base_image

    def update(self):
        self.input()
        self.verificar_delay_ataque()
        self.move(self.speed)

        self.animate()
        self.get_status()
        #debug(self.status, 200, 100)
        #debug(f"Balas: {self.balas if self.arma_visivel else ''}", 10, 10)
        self.desenhar_interface_municao()

    def desenhar_interface_municao(self):
        if self.arma_visivel:
            img_path = f"graphics/weapons/gun/teste/municao_{min(self.balas, 5)}.png"
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (80, 40))
            display_surface = pygame.display.get_surface()
            display_surface.blit(img, (10, 10))

class Bala(pygame.sprite.Sprite):
    def __init__(self, pos, direction, obstacles, status):
        super().__init__()
        if 'up' in status:
            self.image = pygame.image.load('graphics/weapons/gun/bala_up.png').convert_alpha()
        elif 'down' in status:
            self.image = pygame.image.load('graphics/weapons/gun/bala_down.png').convert_alpha()
        elif 'left' in status:
            self.image = pygame.image.load('graphics/weapons/gun/bala_left.png').convert_alpha()
        elif 'right' in status:
            self.image = pygame.image.load('graphics/weapons/gun/bala_right.png').convert_alpha()
        else:
            self.image = pygame.Surface((16, 16), pygame.SRCALPHA)  # fallback invisível

        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.speed = 6
        self.obstacles = obstacles


    def update(self):
        self.rect.center += self.direction * self.speed
        for sprite in self.obstacles:
            if sprite.rect.colliderect(self.rect):
                self.kill()