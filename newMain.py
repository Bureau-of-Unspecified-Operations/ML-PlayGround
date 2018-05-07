

import pygame
import sys
import NeuralNets as nets
import Neurons
import NNDrawer as NND
import jygame as jp
import Colors




class MachineLearningGameLoop(object):

	def __init__(self):
		pygame.init()
		infoObj = pygame.display.Info()
		self.width = infoObj.current_w
		self.height = infoObj.current_h - 60
	
		self.screen = pygame.display.set_mode((self.width, self.height))
		
		print(self.width)
		print(self.height)

		self.models = list()
		self.models.append(nets.Net(4, 3, Neurons.Sigmoid, nets.Net.leastSquaredDerivative,((Neurons.Sigmoid,5))))
		self.frames = self.initFrames(); # might want to be in func init?
		self.viewModels = list()
		self.viewModels.append(NND.NNDrawer(self.frames[0]))



	#basic bitch split it all evenly
	def initFrames(self):
		frames = list()
		cnt = len(self.models)
		spacing = self.width if cnt == 0 else self.width // cnt
		for i in range(cnt):
			print("in range")
			frame = jp.Frame((i * spacing, 0), spacing, self.height, pygame.Surface((spacing, self.height)))
			frame.margin = 10
			frames.append(frame)
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
		self.screen.fill(Colors.RED)
		for frame in self.frames:
			pygame.draw.rect(frame.screen, Colors.GREEN, (frame.x,frame.y,frame.width,frame.height), 0)

		for i in range(len(self.models)):
			viewModel = self.viewModels[i]
			frame = self.frames[i]
			for drawable in viewModel.getDrawables(self.models[i]):
				drawable.draw(frame)

		for frame in self.frames:
			self.screen.blit(frame.screen, (frame.x, frame.y))

	
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