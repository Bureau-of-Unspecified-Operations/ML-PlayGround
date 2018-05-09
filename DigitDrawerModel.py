import jygame as jp


class DigitDrawer(object):

	def __init__(self, n):
		self.grid = jp.util.make2dList(n, n)
		jp.util.fill2dList(self.grid, False)
		self.gridChanged = jp.util.make2dList(n, n)
		jp.util.fill2dList(self.gridChanged, False)
		

	def clearGrid(self):
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