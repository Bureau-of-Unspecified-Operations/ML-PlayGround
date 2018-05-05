

import pygame as py




class MachineLearningGameLoop(object):

	def __init__(self):
		self.models = dict()

		pygame.init()
		infoObj = pygame.display.Info()
		self.width = infoObj.current_w
		self.height = infoObj.current_h
		self.screen = pygame.display.set_mode(self.width, self.height)
		self.frames = self.initFrames();

		

	def initFrames():
		cnt = len(models)
		spacing = self.width // cnt
		for i in range(cnt):
			frame = Frame((i * spacing, 0), pygame.Surface((spacing, self.height)))
			self.frames.append(frame)


	def updateDrawables(self):
		

	def init(self):
		pass

	def step(self):
		pass

	def handleEvents(self):
		pass

	def redraw(self):
		for model in self.models.keys():
			viewModel = self.models[model][0]
			frame = self.models[model][1]
			for drawable in viewModel.getDrawables(model):
				drawable.draw(frame)

		for frame in self.frames:
			self.screen.blit(frame.screen, (frame.x0, frame.y0))
			
		pygame.display.update()

	def run(self):
		init()
		while True:
			handleEvents();
			step();
			redraw();
		return False

game = MachineLearningGameLoop()
game.run()