import pygame
from settings import *
from level import Level
from menu import Menu
from pause import PauseScreen
from shop import Shop  # Importar a classe Shop


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("The Legend of Goobus: Breath of the Baphen")
        self.clock = pygame.time.Clock()
        menu = Menu(self.screen)
        menu.run()
        self.stages = [
            (WORLD_MAP, FORESTBG),
            (DESERT_MAP, 'graphics/tilemap/desertground.png')
        ]
        self.current_stage = 0
        self.level = Level(*self.stages[self.current_stage])
        self.game_paused = False
        self.shop_open = False  # Flag para controlar a abertura da lojinha

    def reset_level(self):
        """Recria completamente o nível atual, reposicionando o jogador e inimigos."""
        # Recriar o nível com o mapa atual
        self.level = Level(*self.stages[self.current_stage])

    def run(self):
        while True:
            if self.game_paused:
                pause_screen = PauseScreen(self.screen, self)
                pause_screen.run()
            elif self.shop_open:
                # Abrir a lojinha se a flag estiver ativa
                shop = Shop(self.screen, self.level.player)
                shop.run()
                self.shop_open = False  # Fechar a lojinha após o uso
            else:
                self.handle_events()
                self.screen.fill('black')
                
                # Verificar se o nível precisa ser recriado após a execução
                should_reset_level = self.level.run()
                if should_reset_level:
                    self.reset_level()
                
                pygame.display.update()
                self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_paused = not self.game_paused
                if event.key == pygame.K_j:
                    # Troca de fase ao apertar J
                    self.current_stage = (self.current_stage + 1) % len(self.stages)
                    self.level = Level(*self.stages[self.current_stage])
                if event.key == pygame.K_y:
                    # Abrir a lojinha ao apertar Y
                    self.shop_open = True