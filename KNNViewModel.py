import KNN
import jygame as jp
import pygame
import math

class KNNView(object):

	def __init__(self, frame):
		self.frame = frame
		self.model = KNN.KNNModel(5)
		self.buttons = list()
		self.declareButtons()
		self.mainCellSize = 20
		self.smallCellSize = 10
		self.cx = frame.width // 2
		self.cy = frame.height // 2
		self.length = min(self.frame.width, self.frame.height)
		self.maxr = self.length // 2 - math.sqrt(2) * 10 * self.smallCellSize // 2
		self.minr = math.sqrt(2) * 10 * self.mainCellSize // 2 + math.sqrt(2) * 10 * self.smallCellSize // 2


	def declareButtons(self):
		self.buttons.append(jp.GenericRectButton(self.model.incK, "+", 10, 10))
		self.buttons.append(jp.GenericRectButton(self.model.decK, "-", 30, 30))

	def quit(self):
		pass

	def getDrawables(self):
		shapes = list()
		shapes.extend(self.buttons)
		shapes.extend(self.drawablesFromKNN())
		return shapes

	def drawablesFromKNN(self):
		shapes = list()
		x, y = self.cx - self.mainCellSize // 2, self.cy - self.mainCellSize // 2
		if(self.model.lastClassified is not None):
			shapes.append(jp.DrawableGridFromArray(self.model.lastClassified, x, y, self.mainCellSize, 10))
		else: shapes.append(jp.DrawableGridFromArray([0] * 100, x, y, self.mainCellSize, 10))

		step = 2 * math.pi / self.model.k

		for i, example in enumerate(self.model.lastHelpExamples):
			print("max %d, min %d"%(self.maxr,self.minr))
			r = jp.util.rescale(self.model.lastHelpDistances[i], 0, math.sqrt(100), self.minr, self.maxr)
			theta = step * i
			(rx, ry) = self.cx + int(r * math.cos(theta)) , self.cy - int(r * math.sin(theta))
			x, y = rx - self.smallCellSize * 10 // 2, ry - self.smallCellSize * 10 // 2
			shapes.append(jp.DrawableGridFromArray(example, x, y, self.smallCellSize, 10))
			print("i %d, r %d, d %d, theta %f, x %d, y %d "%(i,r, self.model.lastHelpDistances[i], theta, x,y))
		return shapes


	def mouseEvent(self, x, y, eventType):
		if eventType == pygame.MOUSEBUTTONDOWN:
			for button in self.buttons:
				if button.inRange(x,y):
					button.onClick()
		pass