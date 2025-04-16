import pygame
import random
from settings import *

class WindParticle:
    """Particula visual que representa o vento na tela"""
    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y
        self.direction = direction  # Vetor de direcao (x, y)
        self.speed = speed
        self.alpha = random.randint(150, 255)  # Transparencia
        self.size = random.randint(1, 3)
        self.lifetime = random.randint(30, 120)  # Duracao da particula em frames
        self.color = (255, 255, 255)  # Cor branca para particulas de areia
        
    def update(self):
        # Mover a particula na direcao do vento
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        
        # Diminuir a transparencia com o tempo
        self.alpha = max(0, self.alpha - 2)
        self.lifetime -= 1
        
        # Retornar True se a particula ainda esta viva
        return self.lifetime > 0 and self.alpha > 0
        
    def draw(self, surface):
        # Criar superficie temporaria para a particula com transparencia
        particle_surf = pygame.Surface((self.size, self.size))
        particle_surf.fill(self.color)
        particle_surf.set_alpha(self.alpha)
        
        # Desenhar a particula na tela
        surface.blit(particle_surf, (self.x, self.y))


class WindSystem:
    """Sistema que gerencia o vento no deserto"""
    def __init__(self, screen):
        self.screen = screen
        self.particles = []
        
        # Estado do vento
        self.direction = pygame.Vector2(0, 0)  # Direcao inicial (sem vento)
        self.strength = 0  # Forca do vento (0 a 1)
        
        # Temporizadores
        self.wind_timer = 0
        self.wind_change_interval = random.randint(300, 600)  # Mudar a cada 5-10 segundos
        self.particle_timer = 0
        
    def update(self):
        # Atualizar temporizador do vento
        self.wind_timer += 1
        
        # Verificar se e hora de mudar o vento
        if self.wind_timer >= self.wind_change_interval:
            self._change_wind()
            self.wind_timer = 0
            self.wind_change_interval = random.randint(300, 600)
            
        # Gerar novas particulas
        self.particle_timer += 1
        if self.particle_timer >= 3 and self.strength > 0:  # Gerar particulas a cada 3 frames se tiver vento
            self._spawn_particles()
            self.particle_timer = 0
            
        # Atualizar particulas existentes
        updated_particles = []
        for particle in self.particles:
            if particle.update():
                updated_particles.append(particle)
        self.particles = updated_particles
        
    def draw(self):
        # Desenhar todas as particulas
        for particle in self.particles:
            particle.draw(self.screen)
            
    def _change_wind(self):
        """Alterar aleatoriamente a direcao e forca do vento"""
        # Possiveis direcoes (direita, esquerda, cima, baixo, diagonais)
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
        
        # Escolher uma direcao aleatoria
        chosen_dir = random.choice(possible_directions)
        self.direction = pygame.Vector2(chosen_dir)
        
        # Definir forca aleatoria
        if chosen_dir == (0, 0):
            self.strength = 0
        else:
            self.strength = random.uniform(0.2, 0.8)
            
        print(f"Vento mudou: Direcao {self.direction}, Forca {self.strength}")
        
    def _spawn_particles(self):
        """Criar novas particulas nas bordas da tela, no lado oposto a direcao do vento"""
        num_particles = int(5 * self.strength)  # Mais particulas para ventos mais fortes
        
        for _ in range(num_particles):
            # Determinar a posicao inicial com base na direcao do vento
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
                
            # Criar a particula
            particle = WindParticle(x, y, (self.direction.x, self.direction.y), 
                                   random.uniform(2, 5) * self.strength)
            self.particles.append(particle)
            
    def get_player_speed_modifier(self):
        """Retorna um modificador de velocidade para o jogador com base na direcao do vento"""
        return self.direction, self.strength 