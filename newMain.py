

import pygame
import sys




class MachineLearningGameLoop(object):

	def __init__(self):
		self.models = list()
		self.viewModels = list()

		pygame.init()
		infoObj = pygame.display.Info()
		self.width = infoObj.current_w
		self.height = infoObj.current_h
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.frames = self.initFrames(); # might want to be in func init?	


	#basic bitch split it all evenly
	def initFrames(self):
		frames = list()
		cnt = len(self.models)
		spacing = self.width if cnt == 0 else self.width // cnt
		for i in range(cnt):
			print("in range")
			frame = Frame((i * spacing, 0), spacing, self.height, pygame.Surface((spacing, self.height)))
			self.frames.append(frame)
		return frames

	def global2Frame(self,x,y):  # dif scope/not in the class?
		for i,frame in enumerate(self.frames):
			if frame.containsCoord(x,y):
				return (i, frame.transform(x,y));


		print("oops, no frame held your coord\n")
		return (-1,(-1,-1))

		

	def init(self):
		pass

	def step(self):
		pass

	def handleEvents(self): #design decision: each thing can only be interacted with via buttons (mouse clicks) key presses are only for the global control
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				for viewModel in self.viewModels:
					viewModel.quit() #yeah, the data model will save it's data, the knn saves nothing, ann saves it's nn (maybe)
				pygame.quit()
				sys.exit()

			elif (event.type == pygame.MOUSEBUTTONDOWN or
				  event.type == pygame.MOUSEBUTTONUP or
				  event.type == pygame.MOUSEMOTION):
				(i, (x,y)) = self.global2Frame(*pygame.mouse.get_pos())
				if i >= 0:
					self.viewModels[i].mouseEvent(x, y, event.type)
				
			elif event.type == pygame.KEYDOWN:
				pass

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