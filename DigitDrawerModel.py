import jygame as jp
import numpy as np


class DigitDrawer(object):

	def __init__(self, n, dataModel):
		self.grid = jp.util.make2dList(n, n)
		jp.util.fill2dList(self.grid, False)
		self.gridChanged = jp.util.make2dList(n, n)
		jp.util.fill2dList(self.gridChanged, False)
		self.dataModel = dataModel
		

	def clearGrid(self):
		print("cleared")
		for row in range(len(self.grid)):
			for col in range(len(self.grid[0])):
				self.grid[row][col] = False
				self.gridChanged[row][col] = False

	def toggleCell(self, row, col):
		self.grid[row][col] = not self.grid[row][col]


	

	def clearGridChanges(self):
		for row in range(len(self.gridChanged)):
			for col in range(len(self.gridChanged[0])):
				self.gridChanged[row][col] = False

	def getVector(self):
		vector = np.zeros(100)
		for row in range(len(self.grid)):
			for col in range(len(self.grid[0])):
				x = 0 if self.grid[row][col] == False else 1
				i = row * 10 + col
				vector[i] = x
		return vector

	def add2Data(self, label):
		vector = self.getVector()
		self.dataModel.add(vector, label)
		self.clearGrid()