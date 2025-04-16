import pygame
from settings import *

class LevelTransition:
    def __init__(self, screen, current_level_name, next_level_name):
        self.screen = screen
        self.current_level_name = current_level_name
        self.next_level_name = next_level_name
        self.font = pygame.font.Font(UI_FONT, 32)
        self.big_font = pygame.font.Font(UI_FONT, 48)
        self.should_transition = False
        
        # Efeito de fade
        self.alpha = 0
        self.fade_speed = 2
        self.fading_in = True
        self.delay_timer = 0
        self.delay_duration = 60
        
        # Superfície para fade
        self.fade_surf = pygame.Surface((WIDTH, HEIGHT))
        self.fade_surf.fill((0, 0, 0))
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        # Verificar se o usuário pressionou espaço ou enter para avançar
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
            self.should_transition = True
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Verificar cliques do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.should_transition = True
    
    def draw(self):
        # Desenhar o fundo escuro com transparência
        self.fade_surf.set_alpha(self.alpha)
        self.screen.blit(self.fade_surf, (0, 0))
        
        # Centralizar os textos
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        
        # Texto principal
        victory_text = self.big_font.render("Nivel Completado!", True, (255, 215, 0))
        victory_rect = victory_text.get_rect(center=(center_x, center_y - 80))
        
        # Texto do nivel concluido
        current_level_text = self.font.render(f"Voce completou: {self.current_level_name}", True, (200, 200, 200))
        current_level_rect = current_level_text.get_rect(center=(center_x, center_y))
        
        # Texto do proximo nivel
        next_level_text = self.font.render(f"Proximo nivel: {self.next_level_name}", True, (200, 200, 200))
        next_level_rect = next_level_text.get_rect(center=(center_x, center_y + 50))
        
        # Texto de instrucao
        if self.alpha > 200:  # So mostrar quando o fade estiver quase completo
            instruction_text = self.font.render("Clique ou pressione ESPACO para continuar", True, (255, 255, 255))
            instruction_rect = instruction_text.get_rect(center=(center_x, center_y + 150))
            self.screen.blit(instruction_text, instruction_rect)
        
        # Desenhar os textos quando o fade estiver suficiente
        if self.alpha > 100:
            self.screen.blit(victory_text, victory_rect)
            self.screen.blit(current_level_text, current_level_rect)
            self.screen.blit(next_level_text, next_level_rect)
    
    def update_fade(self):
        # Controlar o efeito de fade in/out
        if self.fading_in:
            self.alpha = min(255, self.alpha + self.fade_speed)
            if self.alpha >= 255:
                self.fading_in = False
                self.delay_timer = self.delay_duration
        elif self.delay_timer > 0:
            self.delay_timer -= 1
    
    def run(self):
        self.alpha = 0  # Resetar o alpha ao iniciar
        self.fading_in = True
        self.should_transition = False
        
        # Loop principal da tela de transição
        while not self.should_transition:
            self.input()
            self.update_fade()
            self.draw()
            pygame.display.update()
            pygame.time.Clock().tick(FPS)
            
            # Se estamos apenas esperando o clique
            if not self.fading_in and self.delay_timer <= 0:
                pass  # Apenas esperando input do usuário
        
        # Retornar True para indicar que devemos avançar para o próximo nível
        return True 