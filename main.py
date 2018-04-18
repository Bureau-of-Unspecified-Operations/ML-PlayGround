import pygame
import sys
import buttons, Colors



def make2dList(rows, cols):
	a = []
	for row in range(rows):
		a.append([False] * cols);
	return a


#################################
## UTILITY STUFF
#################################
def row2Y(row, data):
	return data.gridCorner[1] + row * data.gridSize
def col2X(col, data):
	return data.gridCorner[0] + col * data.gridSize
def x2Col(x, data):
	return (x - data.gridCorner[0]) // data.gridSize
def y2Row(y, data):
	return (y - data.gridCorner[1]) // data.gridSize




class GridCell(buttons.Button):

	def pressed(self, data):
		row = y2Row(self.y, data) 
		col = x2Col(self.x, data)
		data.grid[row][col] = not data.grid[row][col]


class ClearButton(buttons.Button):
	def pressed(data):
		for row in range(len(data.grid)):
			for col in range(len(data.grid[0])):
				data.grid[row][col] = False;
	def text():
		return "Clear Grid"
"""
class ActionButton(buttons.Button):
	def pressed(data):
		s = input(">> ")
		if(s == "clear"):
			clearCells(data)
		elif(s == "train"):
			label = input("What Number is this?\n")
			addData(label,data)
		elif(s == "predict"):
			s = makePrediction(data)
"""



##################################
## EVENT HANDLING GOODNESS
##################################

def buttonHandler(data,coord):
	x , y = (coord[0], coord[1])
	for button in data.buttonList:
		if button.inBounds(x,y):
			button.pressed(data)




##################################
## DRAWING N 'AT
##################################

def drawGrid(data):
	for row in range(len(data.grid)):
		for col in range(len(data.grid[0])):
			color = Colors.BLACK if (data.grid[row][col] == True) else Colors.WHITE
			rect = (col2X(col, data),row2Y(row, data),data.gridSize,data.gridSize)
			pygame.draw.rect(data.screen,color, rect,0)

def drawButtons(data):
	data
	pass


##################################
## INIT STUFF
##################################

def initGridButtons(data):
	for row in range(len(data.grid)):
		for col in range(len(data.grid[0])):
			x = col2X(col, data)
			y = row2Y(row, data)
			cell = GridCell(x,y,data.gridSize,data.gridSize)
			data.buttonList.append(cell)



def defineGlobals(data):
	data.screenWidth = 500
	data.screenHeight = 500
	data.margin = 5
	data.buttonWidth = 60
	data.buttonHeight = 30
	data.grid = make2dList(10,10);
	data.buttonList = []
	data.gridCorner = (60,60);
	data.gridSize = 40	

def initButtons(data):
	x = data.margin
	y = data.screenHeight - data.margin
	w = data.buttonWidth
	h = data.buttonHeight
	clearButton = ClearButton(x,y,w,h)
	data.buttonList.append(clearButton)
	initGridButtons(data)


##################################
## MAIN LOOP FUNCTIONS
##################################
def init(data):
	defineGlobals(data)
	initButtons(data)
	pygame.init()
	screen = pygame.display.set_mode((data.screenWidth,data.screenHeight))
	data.screen = screen



			

def redraw(data):
	drawGrid(data)
	drawButtons(data)
	pygame.display.update()
	pass


def handleEvents(data):
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			pygame.quit()
			sys.exit()
		elif (event.type == pygame.MOUSEBUTTONDOWN):
			buttonHandler(data,pygame.mouse.get_pos())
		


def main():
	class Obj: pass
	data = Obj()
	init(data)
	while True:
		handleEvents(data);
		redraw(data);
	return False

main()