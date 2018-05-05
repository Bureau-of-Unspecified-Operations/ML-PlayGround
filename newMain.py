

import pygame




class MachineLearningGameLoop(object):

	def __init__(self):
		self.models = list()
		self.viewModels = list()

		pygame.init()
		infoObj = pygame.display.Info()
		self.width = infoObj.current_w
		self.height = infoObj.current_h
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.frames = self.initFrames(); # need to connect frames int that dict		

	def initFrames(self):
		self.frames = list()
		cnt = len(self.models)
		spacing = self.width if cnt == 0 else self.width // cnt
		for i in range(cnt):
			frame = Frame((i * spacing, 0), spacing, self.height, pygame.Surface((spacing, self.height)))
			self.frames.append(frame)

	def global2Frame(x,y):
		for i,frame in enumerate(self.frames):
			if frame.containsCoord(x,y):
				return (i, frame.transform(x,y));
		print("oops, no frame held your coord\n")

		

	def init(self):
		pass

	def step(self):
		pass

	def handleEvents(self):
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):

			elif (event.type == pygame.MOUSEBUTTONDOWN):	

			elif event.type == pygame.MOUSEBUTTONUP:

			elif event.type == pygame.MOUSEMOTION:
				
			elif event.type == pygame.KEYDOWN:
				

	def redraw(self):
		for i in range(len(self.models)):
			viewModel = self.viewModels[i]
			frame = self.frames[i]
			for drawable in viewModel.getDrawables(model):
				drawable.draw(frame)

		for frame in self.frames:
			self.screen.blit(frame.screen, (frame.x0, frame.y0))

		pygame.display.update()

	def run(self):
		self.init()
		while True:
			self.handleEvents();
			self.step();
			self.redraw();
		return False

game = MachineLearningGameLoop()
game.run()