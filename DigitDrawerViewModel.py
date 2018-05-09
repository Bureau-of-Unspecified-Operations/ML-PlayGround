import DigitDrawerModel as ddm
import jygame as jp
import pygame

class DigitDrawerVM(object):

	def __init__(self, frame):
		self.model = ddm.DigitDrawer(10)
		self.cellSize = 40
		self.frame = frame
		self.x = 10
		self.y = 10
		self.isDrawing = False
		self.popUps = list()

	def getDrawables(self):
		shapes = list()
		shapes.append(jp.DrawableGrid(self.model.grid, self.x, self.y, self.cellSize))
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
		elif eventType == pygame.MOUSEBUTTONUP:
			self.isDrawing = False
			self.model.clearGridChanges()
		elif eventType == pygame.MOUSEMOTION:
			if self.isDrawing == True:
				self.colorGrid(x,y)

		
	def quit(self):
		pass