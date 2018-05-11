import DigitDrawerModel as ddm
import jygame as jp
import pygame

class DigitDrawerVM(object):

	def __init__(self, frame, dataModel):
		self.model = ddm.DigitDrawer(10, dataModel)
		self.cellSize = 40
		self.frame = frame
		self.x = 30
		self.y = 10
		self.isDrawing = False
		self.buttons = list()
		self.defineButtons()
		

	def defineButtons(self):
		self.buttons.append(jp.GenericRectButton(self.model.clearGrid, "Clear", self.x, self.y + self.cellSize * 10))
		step = 20
		for i in range(10):
			x = 0
			y = self.y + i * step
			self.buttons.append(LabelButton(self.model.add2Data, str(i), x, y))

	def getDrawables(self):
		shapes = list()
		shapes.append(jp.DrawableGrid(self.model.grid, self.x, self.y, self.cellSize))
		shapes.extend(self.buttons)
		shapes.append(jp.BasicText("Label me please!!", self.x + 60, self.y + self.cellSize * 10, 3, 15))
		return shapes

	def colorGrid(self, x, y):
		for row in range(len(self.model.grid)):
			for col in range(len(self.model.grid[0])):
				if jp.util.inBounds(row,col,x,y, self.cellSize, self.x, self.y) and self.model.gridChanged[row][col] == False:
					self.model.toggleCell(row,col)
					self.model.gridChanged[row][col] = True

	def mouseEvent(self, x, y, eventType):
		if eventType == pygame.MOUSEBUTTONDOWN:
			self.isDrawing = True
			for button in self.buttons:
				if button.inRange(x, y):
					button.onClick()
		elif eventType == pygame.MOUSEBUTTONUP:
			self.isDrawing = False
			self.model.clearGridChanges()
		elif eventType == pygame.MOUSEMOTION:
			if self.isDrawing == True:
				self.colorGrid(x,y)

		
	def quit(self):
		pass

class LabelButton(jp.GenericRectButton):
	def onClick(self):
		self.function(int(self.text))