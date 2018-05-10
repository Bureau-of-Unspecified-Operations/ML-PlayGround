
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
		x0, y0 = 10, self.spacing * 11 + 10
		x1, y1 = 10, self.spacing * 11 + 30 + 10
		self.buttons.append(jp.GenericRectButton(self.model.clearWorkingset, "Clear Working Set", x0, y0))
		self.buttons.append(jp.GenericRectButton(self.model.addAll2Workingset, "add all data to Working Set", x1, y1))

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
		