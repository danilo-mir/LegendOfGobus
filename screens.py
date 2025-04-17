from menu import *
from settings import *
import sys


class ScreenBase:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.buttons = []
        self.running = True

        # Fontes
        self.title_font = pygame.font.Font(UI_FONT, 80)
        self.button_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        raise NotImplementedError("Subclasses must implement handle_events method.")

    def draw(self):
        raise NotImplementedError("Subclasses must implement draw method.")


class DeathScreen(ScreenBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.should_reset_level = False

        # BG
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.fill((0, 0, 0))

        # Botões
        self.buttons = [
            Button("Reiniciar", (WIDTH // 2 - 100, HEIGHT // 2 + 50), (200, 60),
                   self.button_font, (255, 165, 0), (255, 255, 255)),
            Button("Sair", (WIDTH // 2 - 100, HEIGHT // 2 + 130), (200, 60),
                   self.button_font, (255, 165, 0), (255, 255, 255))
        ]

    def run(self):
        super().run()
        return self.should_reset_level

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()

                if self.buttons[0].is_clicked(mouse_pos, mouse_click):
                    self.running = False
                    self.should_reset_level = True

                elif self.buttons[1].is_clicked(mouse_pos, mouse_click):
                    pygame.quit()
                    sys.exit()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        # Titulo
        title_surf = self.title_font.render("FIM DE JOGO", True, (255, 0, 0))
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.screen.blit(title_surf, title_rect)

        # Subtitulo
        subtitle_surf = self.button_font.render("Você morreu!", True, (255, 255, 255))
        subtitle_rect = subtitle_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(subtitle_surf, subtitle_rect)

        # Botões
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, button.is_hovered(mouse_pos))


class PauseScreen(ScreenBase):
    def __init__(self, screen, game):
        super().__init__(screen)
        self.game = game

        # BG
        self.bg = pygame.image.load(BG)
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        self.overlay = pygame.Surface((WIDTH, HEIGHT))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(200)

        # Fontes
        self.title_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE + 20)

        # Botões
        self.buttons = [
            Button("Resume", (WIDTH // 2 - 100, 300), (200, 60),
                   self.button_font, (255, 165, 0), (255, 255, 255)),
            Button("Menu", (WIDTH // 2 - 100, 380), (200, 60),
                   self.button_font, (255, 165, 0), (255, 255, 255)),
            Button("Quit", (WIDTH // 2 - 100, 460), (200, 60),
                   self.button_font, (255, 165, 0), (255, 255, 255))
        ]

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

            if not self.game.game_paused:
                break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()

                if self.buttons[0].is_clicked(mouse_pos, mouse_click):
                    self.game.game_paused = False

                elif self.buttons[1].is_clicked(mouse_pos, mouse_click):
                    self.game.game_paused = False
                    menu = Menu(self.screen)
                    menu.run()

                elif self.buttons[2].is_clicked(mouse_pos, mouse_click):
                    pygame.quit()
                    sys.exit()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.overlay, (0, 0))

        # Titulo
        title_surface = self.title_font.render("Game Paused", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 180))
        self.screen.blit(title_surface, title_rect)

        # Botões
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, button.is_hovered(mouse_pos))


class Shop(ScreenBase):
    def __init__(self, screen, player):
        super().__init__(screen)  # Usa a lógica padrão da ScreenBase
        self.player = player

        # Fundo e overlay
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.fill((30, 30, 50))
        self.overlay = pygame.Surface((WIDTH, HEIGHT))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(150)

        # Fontes (pode sobrescrever as da base se quiser)
        self.title_font = pygame.font.Font(UI_FONT, 40)
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

        # Feedback
        self.feedback_message = ""
        self.feedback_color = (255, 255, 255)
        self.feedback_timer = 0

    def run(self):
        super().run()  # Usa loop padrão da base

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_LCTRL):
                    self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()

                if self.buttons[0].is_clicked(mouse_pos, mouse_click):
                    self.buy_ammo()
                elif self.buttons[1].is_clicked(mouse_pos, mouse_click):
                    self.steal_from_shop()
                elif self.buttons[2].is_clicked(mouse_pos, mouse_click):
                    self.running = False

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        # Título
        title_surf = self.title_font.render("LOJINHA DO URUB'UZON", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//4))
        self.screen.blit(title_surf, title_rect)

        # Info do jogador
        coins_surf = self.info_font.render(f"Moedas: {self.player.coins}", True, (255, 255, 255))
        coins_rect = coins_surf.get_rect(center=(WIDTH//2, HEIGHT//4 + 50))
        self.screen.blit(coins_surf, coins_rect)

        ammo_surf = self.info_font.render(f"Municao: {self.player.ammo}/{self.player.max_ammo}", True, (255, 255, 255))
        ammo_rect = ammo_surf.get_rect(center=(WIDTH//2, HEIGHT//4 + 80))
        self.screen.blit(ammo_surf, ammo_rect)

        # Botões
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.draw(self.screen, button.is_hovered(mouse_pos))

        # Feedback
        if self.feedback_timer > 0:
            feedback_surf = self.info_font.render(self.feedback_message, True, self.feedback_color)
            feedback_rect = feedback_surf.get_rect(center=(WIDTH//2, HEIGHT - 100))
            self.screen.blit(feedback_surf, feedback_rect)

        # Timer
        if self.feedback_timer > 0:
            self.feedback_timer -= 1

    def buy_ammo(self):
        coin_cost = 3
        if self.player.coins >= coin_cost:
            if self.player.ammo >= self.player.max_ammo:
                self.show_feedback("Municao ja esta cheia!", (255, 165, 0))
                return
            success = self.player.spend_coins(coin_cost)
            if success:
                self.player.ammo = min(self.player.ammo + 1, self.player.max_ammo)
                self.show_feedback("Compra bem-sucedida! +1 bala", (0, 255, 0))
        else:
            self.show_feedback("Moedas insuficientes! Precisa de 3 moedas.", (255, 0, 0))

    def steal_from_shop(self):
        if self.player.ammo >= self.player.max_ammo:
            self.show_feedback("Municao ja esta cheia!", (255, 165, 0))
            return
        self.player.steal_from_shop()
        self.player.ammo = min(self.player.ammo + 2, self.player.max_ammo)
        thief_level = self.player.thief_count
        penalty_percentage = int((1 - 0.95**thief_level) * 100)
        self.show_feedback(f"Voce roubou a loja! -5% de destreza #{thief_level} (total: -{penalty_percentage}%)", (255, 0, 0))

    def show_feedback(self, message, color=(255, 255, 255)):
        self.feedback_message = message
        self.feedback_color = color
        self.feedback_timer = 180
