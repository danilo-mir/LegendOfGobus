import pygame, sys
from settings import *
from nivel import *

class Game:
	def __init__(self):
		  
		# general setup
		pygame.init() #iniciando pygame
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH)) # criandoa tela
		pygame.display.set_caption('LegendOfGobus')
		self.clock = pygame.time.Clock() # criando o relógio

		self.nivel = Nivel()

	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: #cheackando se o jogo foi fechado
					pygame.quit()
					sys.exit()

			self.screen.fill('white')
			self.nivel.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()