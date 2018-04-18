import pygame
import sys
import buttons, Colors
import KNN
import pickle
from pathlib import Path

dataPath = "digitVectors.p"
labelsPath = "digitLabels.p"


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




dataFile = Path(dataPath)
labelFile = Path(labelsPath)
if dataFile.is_file():
	print("data exists")
	data = pickle.load(open(dataPath, "rb"))
	labels = pickle.load(open(labelsPath, "rb"))
	print("data size: %d"%len(data))
else:
	data = []
	labels = []

knn = KNN.KNN(3, data, labels)

def saveData():
	print("data save size: %d"%len(knn.data))
	pickle.dump(knn.data , open(dataPath, "wb"))
	pickle.dump(knn.labels, open(labelsPath, "wb"))


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

################################
## ML STUFF
################################
def grid2Vector(grid):
	vector = []
	for row in range(len(grid)):
		for col in range(len(grid[0])):
			x = 0 if grid[row][col] == False else 1
			vector.append(x)

def train(data, val):
	vector = grid2Vector(data.grid)
	label = int(val)
	knn.train(vector,label)

def classify(data):
	print("42...")
	

#################################
## COMMAND FLOW
#################################

def commandMode(data):
	x = input(">> ")
	if x == "clear":
		clearGrid(data)
	elif x == "train":
		val = input("What digit is this?\n")
		train(data,val)
		clearGrid(data)
	elif x == "pred":
		p = classify(data)
		print("Robot thinks it's %s"%p)
		val = input("\nWas it right? input which digit it was\n")
		train(data,val)
		clearGrid(data)
	pass


##################################
## EVENT HANDLING GOODNESS
##################################

def clearGrid(data):
	for row in range(len(data.grid)):
		for col in range(len(data.grid[0])):
			data.grid[row][col] = False
			data.gridChanged[row][col] = False

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
			saveData()
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