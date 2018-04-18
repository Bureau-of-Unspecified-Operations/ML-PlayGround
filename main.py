import pygame
import sys
import buttons, Colors



def make2dList(rows, cols):
	a = []
	for row in range(rows):
		a.append([False] * cols);
	return a

# destructive
def fill2dList(l,val):
	for row in range(len(l)):
		for col in range(len(l[0])):
			l[row][col] = val


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

#################################
## COMMAND FLOW
#################################

def commandMode(data):
	
	pass


##################################
## EVENT HANDLING GOODNESS
##################################



def toggleCell(data, row, col):
	data.grid[row][col] = not data.grid[row][col]

def inBounds(data, row, col, x, y):
	x0 = col2X(col, data)
	y0 = row2Y(row, data)
	return (x0 <= x and x <= x0 + data.gridSize and
			y0 <= y and y <= y0 + data.gridSize)

def colorGrid(data, coord):
	x , y = (coord[0], coord[1])
	for row in range(len(data.grid)):
		for col in range(len(data.grid[0])):
			if inBounds(data,row,col,x,y) and data.gridChanged[row][col] == False:
				toggleCell(data,row,col)
				data.gridChanged[row][col] = True

def clearGridChanges(data):
	for row in range(len(data.gridChanged)):
		for col in range(len(data.gridChanged[0])):
			data.gridChanged[row][col] = False




##################################
## DRAWING N 'AT
##################################

def drawGrid(data):
	for row in range(len(data.grid)):
		for col in range(len(data.grid[0])):
			color = Colors.BLACK if (data.grid[row][col] == True) else Colors.WHITE
			rect = (col2X(col, data),row2Y(row, data),data.gridSize,data.gridSize)
			pygame.draw.rect(data.screen,color, rect,0)




##################################
## INIT STUFF
##################################




def defineGlobals(data):
	data.screenWidth = 500
	data.screenHeight = 500
	data.margin = 5
	data.buttonWidth = 60
	data.buttonHeight = 30
	data.grid = make2dList(10,10);
	data.gridChanged = make2dList(10,10)
	data.buttonList = []
	data.gridCorner = (60,60);
	data.gridSize = 40	
	data.buttonDown = False


##################################
## MAIN LOOP FUNCTIONS
##################################
def init(data):
	defineGlobals(data)
	pygame.init()
	screen = pygame.display.set_mode((data.screenWidth,data.screenHeight))
	data.screen = screen
			

def redraw(data):
	drawGrid(data)
	pygame.display.update()
	pass


def handleEvents(data):
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			pygame.quit()
			sys.exit()

		elif (event.type == pygame.MOUSEBUTTONDOWN):
			data.buttonDown = True

		elif event.type == pygame.MOUSEBUTTONUP:
			data.buttonDown = False
			clearGridChanges(data)

		elif event.type == pygame.MOUSEMOTION:
			if data.buttonDown == True:
				colorGrid(data, pygame.mouse.get_pos())
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				commandMode(data)
		


def main():
	class Obj: pass
	data = Obj()
	init(data)
	while True:
		handleEvents(data);
		redraw(data);
	return False

main()