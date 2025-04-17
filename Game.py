import pygame
from settings import *
from level import Level
from screens import PauseScreen, Shop, Menu, WinScreen
from level_transition import LevelTransition


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
            (DESERT_MAP, DESERTBG),
            (ICE_MAP, ICEBG),
            (VOLCANO_MAP, VOLCANOBG)
        ]
        self.stage_names = ["Floresta", "Deserto", "Lago Congelado", "Vulcão"]  # Nomes das fases
        self.current_stage = 0
        self.level = Level(*self.stages[self.current_stage])
        self.game_paused = False
        self.shop_open = False  # Flag para controlar a abertura da lojinha
        self.level_transition_active = False  # Flag para controlar a transição de níveis
        
        # Sistema de mensagens
        self.message = ""
        self.message_color = (255, 255, 255)
        self.message_timer = 0
        self.font = pygame.font.Font(UI_FONT, 32)

    def show_message(self, text, color=(255, 255, 255), duration=180):
        """Mostrar uma mensagem temporária na tela"""
        self.message = text
        self.message_color = color
        self.message_timer = duration

    def reset_level(self):
        """Recria completamente o nível atual, reposicionando o jogador e inimigos."""
        self.level = Level(*self.stages[self.current_stage])
        
    def advance_to_next_level(self):
        """Avança para o próximo nível"""
        current_name = self.stage_names[self.current_stage]
        
        if self.current_stage == 3:
            transition = WinScreen(self.screen)
            transition.run()

        # Avançar para o próximo nível
        self.current_stage = (self.current_stage + 1) % len(self.stages)
        next_name = self.stage_names[self.current_stage]

        # Mostrar a tela de transição
        self.level_transition_active = True
        transition = LevelTransition(self.screen, current_name, next_name)
        if transition.run():
            # Se a transição foi concluída, carregar o próximo nível
            self.level = Level(*self.stages[self.current_stage])
            self.level_transition_active = False
            # self.show_message(f"Fase: {next_name}", (255, 215, 0), 180)

    def run(self):
        while True:
            if self.game_paused:
                pause_screen = PauseScreen(self.screen, self)
                pause_screen.run()
            elif self.level_transition_active:
                # Se estiver em transição de nível, não fazer nada até que seja concluído
                pass
            elif self.shop_open:
                # Abrir a lojinha se a flag estiver ativa
                shop = Shop(self.screen, self.level.player)
                shop.run()
                self.shop_open = False  # Fechar a lojinha após o uso
            else:
                self.handle_events()
                self.screen.fill('black')
                
                # Executar o nível e verificar se ele foi concluído
                should_reset_level = self.level.run()
                
                # Se o nível foi concluído (todos os inimigos derrotados), avançar
                if self.level.level_completed:
                    self.advance_to_next_level()
                # Se o jogador morreu, reiniciar o nível
                elif should_reset_level:
                    self.reset_level()
                
                # Mostrar mensagem temporária se o timer estiver ativo
                if self.message_timer > 0:
                    self.message_timer -= 1
                    msg_surf = self.font.render(self.message, True, self.message_color)
                    msg_rect = msg_surf.get_rect(center=(WIDTH//2, HEIGHT - 100))
                    pygame.draw.rect(self.screen, (0, 0, 0, 128), msg_rect.inflate(20, 10))
                    self.screen.blit(msg_surf, msg_rect)
                
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
                if event.key == pygame.K_LCTRL:
                    # Abrir a lojinha ao apertar Y
                    self.shop_open = True