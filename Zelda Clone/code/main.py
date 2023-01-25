import pygame, sys
from settings import* #pega os valores do arquivo settings
from level import Level

class Game:
	def __init__(self):
		
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption('Zelda Clone')
		self.clock = pygame.time.Clock()

		self.level = Level()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
 	game = Game() #instancia o jogo
 	game.run()