import pygame
import sys
from settings import *
from menu import Button

class Shop:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Fundo
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.fill((30, 30, 50))  # Fundo azul escuro para a lojinha
        self.overlay = pygame.Surface((WIDTH, HEIGHT))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(150)
        
        # Fontes
        self.title_font = pygame.font.Font(UI_FONT, 40)
        self.button_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.info_font = pygame.font.Font(UI_FONT, 24)
        
        # Botões
        button_width = 300
        button_height = 60
        self.buttons = [
            Button("Comprar Balas (3 moedas)", (WIDTH//2 - button_width//2, HEIGHT//2 - 80), 
                   (button_width, button_height), self.button_font, (255, 215, 0), (255, 255, 255)),
            Button("Roubar Loja (Penalidade)", (WIDTH//2 - button_width//2, HEIGHT//2 + 10), 
                   (button_width, button_height), self.button_font, (255, 0, 0), (255, 255, 255)),
            Button("Sair", (WIDTH//2 - button_width//2, HEIGHT//2 + 100), 
                   (button_width, button_height), self.button_font, (255, 165, 0), (255, 255, 255))
        ]
        
        # Mensagem de feedback
        self.feedback_message = ""
        self.feedback_color = (255, 255, 255)
        self.feedback_timer = 0
        
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
            
            # Atualizar temporizador de feedback
            if self.feedback_timer > 0:
                self.feedback_timer -= 1
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_LCTRL:
                    self.running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()
                
                # Botão Comprar Balas
                if self.buttons[0].is_clicked(mouse_pos, mouse_click):
                    self.buy_ammo()
                
                # Botão Roubar Loja
                elif self.buttons[1].is_clicked(mouse_pos, mouse_click):
                    self.steal_from_shop()
                
                # Botão Sair
                elif self.buttons[2].is_clicked(mouse_pos, mouse_click):
                    self.running = False
                    
    def buy_ammo(self):
        """Tentar comprar balas usando moedas"""
        coin_cost = 3
        
        # Verificar se o jogador tem moedas suficientes
        if self.player.coins >= coin_cost:
            # Verificar se o jogador já tem munição cheia
            if self.player.ammo >= self.player.max_ammo:
                self.show_feedback("Municao ja esta cheia!", (255, 165, 0))
                return
                
            # Gastar moedas e adicionar munição
            success = self.player.spend_coins(coin_cost)
            if success:
                self.player.ammo = min(self.player.ammo + 1, self.player.max_ammo)
                self.show_feedback("Compra bem-sucedida! +1 bala", (0, 255, 0))
        else:
            self.show_feedback("Moedas insuficientes! Precisa de 3 moedas.", (255, 0, 0))
            
    def steal_from_shop(self):
        """Roubar a loja para ganhar municao, mas sofrer penalidades permanentes"""
        # Verificar se o jogador já tem munição cheia
        if self.player.ammo >= self.player.max_ammo:
            self.show_feedback("Municao ja esta cheia!", (255, 165, 0))
            return
            
        # Roubar a loja (adicionar munição e aplicar penalidade)
        self.player.steal_from_shop()
        # Adicionar mais balas do que na compra normal
        self.player.ammo = min(self.player.ammo + 2, self.player.max_ammo)
        
        thief_level = self.player.thief_count
        
        # Mensagem informando a penalidade
        penalty_percentage = int((1 - 0.95**thief_level) * 100)
        self.show_feedback(f"Voce roubou a loja! -5% de destreza #{thief_level} (total: -{penalty_percentage}%)", (255, 0, 0))
            
    def show_feedback(self, message, color=(255, 255, 255)):
        """Mostrar mensagem de feedback temporária"""
        self.feedback_message = message
        self.feedback_color = color
        self.feedback_timer = 180
            
    def draw(self):
        # Desenhar fundo
        self.screen.blit(self.bg, (0, 0))
        
        # Desenhar título
        title_surf = self.title_font.render("LOJINHA DO URUB'UZON", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//4))
        self.screen.blit(title_surf, title_rect)
        
        # Desenhar informações do jogador
        coins_surf = self.info_font.render(f"Moedas: {self.player.coins}", True, (255, 255, 255))
        coins_rect = coins_surf.get_rect(center=(WIDTH//2, HEIGHT//4 + 50))
        self.screen.blit(coins_surf, coins_rect)
        
        ammo_surf = self.info_font.render(f"Municao: {self.player.ammo}/{self.player.max_ammo}", True, (255, 255, 255))
        ammo_rect = ammo_surf.get_rect(center=(WIDTH//2, HEIGHT//4 + 80))
        self.screen.blit(ammo_surf, ammo_rect)
        
        # Desenhar botões
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, button.is_hovered(mouse_pos))
            
        # Desenhar mensagem de feedback se o timer estiver ativo
        if self.feedback_timer > 0:
            feedback_surf = self.info_font.render(self.feedback_message, True, self.feedback_color)
            feedback_rect = feedback_surf.get_rect(center=(WIDTH//2, HEIGHT - 100))
            self.screen.blit(feedback_surf, feedback_rect) 