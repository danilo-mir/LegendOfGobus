# Game.py

import pygame
from settings import *
from level import Level
from menu import Menu


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("The Legend of Goobus: Breath of the Baphen")
        self.clock = pygame.time.Clock()

        # Show menu first
        menu = Menu(self.screen)
        menu.run()

        # You can optionally use menu.get_volume_settings() to configure volume
        # music_vol, sfx_vol = menu.get_volume_settings()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
