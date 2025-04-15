import pygame
from settings import *
from level import Level
from menu import Menu
from pause import PauseScreen


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("The Legend of Goobus: Breath of the Baphen")
        self.clock = pygame.time.Clock()
        menu = Menu(self.screen)
        menu.run()
        self.level = Level()
        self.game_paused = False

    def run(self):
        while True:
            if self.game_paused:
                pause_screen = PauseScreen(self.screen, self)
                pause_screen.run()
            else:
                self.handle_events()
                self.screen.fill('black')
                self.level.run()
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