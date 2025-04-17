import pygame
import random
from settings import *


class WindParticle:
    """Partícula visual que representa o vento na tela"""
    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y
        self.direction = direction  # Vetor de direção (x, y)
        self.speed = speed
        self.alpha = random.randint(150, 255)  # Transparência
        self.size = random.randint(1, 3)
        self.lifetime = random.randint(30, 120)  # Duração da partícula em frames
        self.color = (255, 255, 255)  # Cor branca para partículas de areia
        
    def update(self):
        # Mover a partícula na direção do vento
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        
        # Diminuir a transparência com o tempo
        self.alpha = max(0, self.alpha - 2)
        self.lifetime -= 1
        
        # Retornar True se a partícula ainda está viva
        return self.lifetime > 0 and self.alpha > 0
        
    def draw(self, surface):
        # Criar superfície temporária para a partícula com transparência
        particle_surf = pygame.Surface((self.size, self.size))
        particle_surf.fill(self.color)
        particle_surf.set_alpha(self.alpha)
        
        # Desenhar a partícula na tela
        surface.blit(particle_surf, (self.x, self.y))


class WindSystem:
    """Sistema que gerencia o vento no deserto"""
    def __init__(self, screen):
        self.screen = screen
        self.particles = []
        
        # Estado do vento
        self.direction = pygame.Vector2(0, 0)  # Direção inicial (sem vento)
        self.strength = 0  # Força do vento (0 a 1)
        
        # Temporizadores
        self.wind_timer = 0
        self.wind_change_interval = random.randint(300, 600)  # Mudar a cada 5-10 segundos
        self.particle_timer = 0
        
    def update(self):
        # Atualizar temporizador do vento
        self.wind_timer += 1
        
        # Verificar se é hora de mudar o vento
        if self.wind_timer >= self.wind_change_interval:
            self._change_wind()
            self.wind_timer = 0
            self.wind_change_interval = random.randint(300, 600)
            
        # Gerar novas partículas
        self.particle_timer += 1
        if self.particle_timer >= 3 and self.strength > 0:  # Gerar partículas a cada 3 frames se tiver vento
            self._spawn_particles()
            self.particle_timer = 0
            
        # Atualizar partículas existentes
        updated_particles = []
        for particle in self.particles:
            if particle.update():
                updated_particles.append(particle)
        self.particles = updated_particles
        
    def draw(self):
        # Desenhar todas as partículas
        for particle in self.particles:
            particle.draw(self.screen)
            
    def _change_wind(self):
        """Alterar aleatoriamente a direção e força do vento"""
        # Possíveis direções (direita, esquerda, cima, baixo, diagonais)
        possible_directions = [
            (1, 0),    # direita
            (-1, 0),   # esquerda
            (0, 1),    # baixo
            (0, -1),   # cima
            (0.7, 0.7),   # diagonal baixo-direita
            (-0.7, 0.7),  # diagonal baixo-esquerda
            (0.7, -0.7),  # diagonal cima-direita
            (-0.7, -0.7), # diagonal cima-esquerda
            (0, 0)     # sem vento
        ]
        
        # Escolher uma direção aleatória
        chosen_dir = random.choice(possible_directions)
        self.direction = pygame.Vector2(chosen_dir)
        
        # Definir força aleatória
        if chosen_dir == (0, 0):
            self.strength = 0
        else:
            self.strength = random.uniform(0.2, 0.8)
            
        print(f"Vento mudou: Direçao {self.direction}, Força {self.strength}")
        
    def _spawn_particles(self):
        """Criar novas partículas nas bordas da tela, no lado oposto à direção do vento"""
        num_particles = int(5 * self.strength)  # Mais partículas para ventos mais fortes
        
        for _ in range(num_particles):
            # Determinar a posição inicial com base na direção do vento
            if self.direction.x > 0:  # Vento da esquerda para a direita
                x = random.randint(0, 50)
            elif self.direction.x < 0:  # Vento da direita para a esquerda
                x = random.randint(WIDTH - 50, WIDTH)
            else:
                x = random.randint(0, WIDTH)
                
            if self.direction.y > 0:  # Vento de cima para baixo
                y = random.randint(0, 50)
            elif self.direction.y < 0:  # Vento de baixo para cima
                y = random.randint(HEIGHT - 50, HEIGHT)
            else:
                y = random.randint(0, HEIGHT)
                
            # Criar a partícula
            particle = WindParticle(x, y, (self.direction.x, self.direction.y), 
                                   random.uniform(2, 5) * self.strength)
            self.particles.append(particle)
            
    def get_player_speed_modifier(self):
        """Retorna um modificador de velocidade para o jogador com base na direção do vento"""
        return self.direction, self.strength 