


class DigitDrawer(object):

	def __init__(self, n):
		self.grid = jp.util.make2dList(n,n)
		jp.util.fill2dList(self.grid, False)
		self.gridChange = jp.util.make2dList(n.n)
		jp.util.fill2dList(self.gridChanged, False)

	def clearGrid(self):
	for row in range(len(self.grid)):
		for col in range(len(self.grid[0])):
			self.grid[row][col] = False
			self.gridChanged[row][col] = False

	def toggleCell(self, row, col):
		self.grid[row][col] = not self.grid[row][col]


	def colorGrid(self, coord):
		x , y = (coord[0], coord[1])
		for row in range(len(self.grid)):
			for col in range(len(self.grid[0])):
				if jp.util.inBounds(data,row,col,x,y) and self.gridChanged[row][col] == False:
					self.toggleCell(data,row,col)
					self.gridChanged[row][col] = True

	def clearGridChanges(self):
		for row in range(len(self.gridChanged)):
			for col in range(len(self.gridChanged[0])):
				self.gridChanged[row][col] = False