import pygame
import sys
import buttons

BLACK = (0,0,0)
WHITE = (255,2,255)


def make2dList(rows, cols):
	a = []
	for row in range(rows):
		a.append([False] * cols);
	return a


grid = make2dList(10,10);
buttonList = []
gridCorner = (0,0);
gridSize = 40

def row2Y(row):
	return gridCorner[1] + row * gridSize
def col2X(col):
	return gridCorner[0] + col * gridSize
def x2Col(x):
	return (x - gridCorner[0]) // gridSize
def y2Row(y):
	return (y - gridCorner[1]) // gridSize


class GridSquare(buttons.Button):

	def pressed(self):
		row = y2Row(self.y) 
		col = x2Col(self.x)
		print("row: %d, col: %d \n"%(row,col))
		grid[row][col] = not grid[row][col]



##################################
## EVENT HANDLING GOODNESS
##################################

def buttonHandler(coord):
	x , y = (coord[0], coord[1])
	#print("x coord: %d y coord: %d"%(x,y))
	for button in buttonList:
		if button.inBounds(x,y):
			button.pressed()




##################################
## DRAWING N 'AT
##################################

def drawGrid(data):
	for row in range(len(grid)):
		for col in range(len(grid[0])):
			color = BLACK if (grid[row][col] == True) else WHITE
			rect = (col2X(col),row2Y(row),gridSize,gridSize)
			pygame.draw.rect(data.screen,color, rect,0)

##################################
## INIT STUFF
##################################

def initGridButtons():
	for row in range(len(grid)):
		for col in range(len(grid[0])):
			x = col2X(col)
			y = row2Y(row)
			#print("button x: %d, y: %d \n"%(x,y))
			button = GridSquare(x,y,gridSize,gridSize)
			buttonList.append(button)


##################################
## MAIN LOOP FUNCTIONS
##################################
def init(data):
	initGridButtons()
	pygame.init()
	screen = pygame.display.set_mode((400,400))
	data.screen = screen



			

def redraw(data):
	drawGrid(data);
	pygame.display.update()
	pass


def handleEvents(data):
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			pygame.quit()
			sys.exit()
		elif (event.type == pygame.MOUSEBUTTONDOWN):
			buttonHandler(pygame.mouse.get_pos())
		


def main():
	class Obj: pass
	data = Obj()
	init(data)
	while True:
		handleEvents(data);
		redraw(data);
	return False

main()