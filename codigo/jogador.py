import pygame
from settings import*
from debug import *

class Jogador(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.atacando = False
        self.tempo_delay_ataque = 400
        self.tempo_ataque = None

        self.obstacle_sprites = obstacle_sprites
        self.status = "center"
        """
        def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'up_idle': [],
            'down_idle': [],
            'left_idle': [],
            'right_idle': [],
            'up_attack': [],
            'down_attack': [],
            'left_attack': [],
            'right_attack': [],
        }"""


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
        
        #comando de tiro
        if keys[pygame.K_x] and not self.atacando:
            self.atacando = True
            self.tempo_ataque = pygame.time.get_ticks()
            #usando tempo_ataque aqui tb, pra poder usar a msm variavel
            #na funcao delay

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
            if not '_parado' in self.status and not 'atacando in self.status':
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

    def update(self):
        self.input()
        self.verificar_delay_ataque()
        self.move(self.speed)

        self.get_status()
        debug(self.status, 200, 100)