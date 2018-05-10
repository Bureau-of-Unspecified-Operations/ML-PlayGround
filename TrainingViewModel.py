import TestTrainModel as TTM
import jygame as jp
import pygame

class TestTrainView(object):
	def __init__(self, algo, drawer, data):
		self.model = TTM.TestTrainModel(algo, drawer, data)
		self.buttons = list()
		self.errorMatrix = list()
		self.pred = list()
		self.control = dict()
		self.control["showError"] = False
		self.control["showPred"] = False
		self.declareButtons()
		self.labels = [str(i) for i in range(10)]

	def declareButtons(self):
		x0 = x1 = x2 = 10
		y0 = 10
		y1 = 40
		y2 = 70
		self.buttons.append(TestSingle(self.model.testOnSingle, "Test on Single", x0, y0, self.control, self.pred))
		self.buttons.append(CrossVal(self.model.crossWrapper, "CrossVal on Workingset", x1, y1, self.control, self.errorMatrix))
		self.buttons.append(Train(self.model.testOnSingle, "Train on workingset", x2, y2, self.control))


	def mouseEvent(self, x, y, eventType):
		if eventType == pygame.MOUSEBUTTONDOWN:
			for button in self.buttons:
				if button.inRange(x,y):
					button.onClick()
		pass


	def getDrawables(self):
		shapes = list()
		shapes.extend(self.buttons)
		if self.control["showError"]:
			drawable = jp.DrawableErrorGrid(self.errorMatrix[0], 10, 100, 40, self.labels)
			shapes.append(drawable)
		if self.control["showPred"]:
			drawable = jp.basicText(self.pred[0], 10, 100, 5) # x y margin
			shapes.append(drawable)
		return shapes


	def quit(self):
		pass

class CrossVal(jp.GenericRectButton):
	def __init__(self, function, text, x, y, control, matrixList):
		super().__init__(function, text, x, y)
		self.control = control
		self.matrixList = matrixList

	def onClick(self):
		print("in here")
		(err, preMatrix) = self.function()
		self.control["showError"] = True
		self.control["showPred"] = False
		del self.matrixList[:]
		self.matrixList.append(preMatrix)



class Train(jp.GenericRectButton):
	def __init__(self, function, text, x, y, control):
		super().__init__(function, text, x, y)
		self.control = control

	def onClick(self):
		self.function()
		self.control["showError"] = False
		self.control["showPred"] = False

class TestSingle(jp.GenericRectButton):
	def __init__(self, function, text, x, y, control, predList):
		super().__init__(function, text, x, y)
		self.control = control
		self.predList = predList

	def onClick(self):
		pred = self.function()
		self.control["showError"] = False
		self.control["showPred"] = True
		del self.predList[:]
		self.predList.append(pred)