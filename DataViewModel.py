
import DataModel as dm
import jygame as jp
import pygame

class DataView(object):

	def __init__(self, frame):
		self.model = dm.DataModel()
		self.frame = frame
		self.buttons = list()
		self.spacing = 15
		self.declareButtons()
		self.popUp = list()

	def declareButtons(self):
		rect0 = (10, self.spacing * 11 + 10, 90, 20)
		rect1 = (10, self.spacing * 11 + 30 + 10, 90, 20)
		self.buttons.append(jp.GenericRectButton(self.model.clearWorkingset, "Clear Working Set", rect0))
		self.buttons.append(jp.GenericRectButton(self.model.addAll2Workingset, "add all data to Working Set", rect1))

	def getDrawables(self):
		shapes = list()
		freqTable = self.model.getFrequencyTable()
		shapes.append(jp.FrequencyTable(freqTable, 10, 10, self.spacing))  #MAGIC NUMB
		shapes.extend(self.buttons)
		return shapes;

	def mouseEvent(self, x, y, eventType):
		if eventType == pygame.MOUSEBUTTONDOWN:
			for button in self.buttons:
				if button.inRange(x,y):
					button.onClick()

	def quit(self):
		self.model.save()
		