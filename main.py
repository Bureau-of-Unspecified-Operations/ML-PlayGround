import pygame
import sys
import buttons, Colors
import KNN, NeuralNets, Neurons
import pickle
from pathlib import Path
import numpy as np
import knnError
from jygame import util

dataPath = "digitVectors.p"
labelsPath = "digitLabels.p"
dataPath0 = "dataset.p"


class Frame(object): pass

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



dataFile0 = Path(dataPath0)
if dataFile0.is_file():
	dataset = pickle.load(open(dataPath0, "rb"))

else:
	dataset = [(datas[i], labels[i]) for i in range(len(datas))]

#net = NeuralNets.Net(100,5,10)

knn = KNN.KNN(5)
tester = knnError.KNNTester(knn)

#net = NeuralNets.Net(100,10,Neurons.Softmax(),NeuralNets.Net.crossEntropy,(Neurons.Sigmoid(), 10))

def newSaveData():
	pickle.dump(dataset, open(dataPath0, "wb"))


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
	return vector


def train(data, val):
	vector = grid2Vector(data.grid)
	label = int(val)
	dataset.append((vector,label))



def classify(data):
	vector = grid2Vector(data.grid)
	(pred, metaData) = knn.classify(dataset, vector)
	changeGuesses(data, metaData)
	data.drawNeighbors = True
	data.showError = False
	return pred
"""
def softMaxLabel(val):
	arr = np.zeros(10);
	arr[int(val)] = 1
	return arr

def netTrain():
	vectors = np.array(datas)
	f_labels = np.zeros((len(datas),10))
	for i in range(len(f_labels)):
		f_labels[i] = softMaxLabel(labels[i])
	net.train(vectors,f_labels)
	print("done!")

def netClassify(data):
	vector = grid2Vector(data.grid)
	return net.adapterCompute(vector)
"""

	

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
		#1111clearGrid(data)
	elif x == "cross":
		(err, matrix) = tester.crossValidate(15, dataset)
		data.showError = True
		data.drawNeighbors = False
		data.matrix = matrix
		#print("err = %d\n"%err)
		#print(matrix)
	"""elif x == "ntrain":
		netTrain()
		clearGrid(data)
	elif x == "npred":
		p = netClassify(data)
		print("Robot thinks it's %s"%p)
		val = input("\nWas it right? input which digit it was\n")
		clearGrid(data)"""
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

def changeGuesses(data, usedData):
	for i in range(data.k):
		data.usedExamples[i] = usedData[i][0]
		data.usedLabels[i] = usedData[i][1]
		data.usedDistance[i] = usedData[i][2]




##################################
## DRAWING N 'AT
##################################


def drawGrid(data):
	for row in range(len(data.grid)):
		for col in range(len(data.grid[0])):
			color = Colors.BLACK if (data.grid[row][col] == True) else Colors.WHITE
			rect = (col2X(col, data),row2Y(row, data),data.gridSize,data.gridSize)
			pygame.draw.rect(data.screen,color, rect,0)

def drawGridFromArray(data, array, x, y, cellSize):
	for i in range(len(array)):
		row = i // 10
		col = i % 10
		x0 = x + col * cellSize
		y0 = y + row * cellSize
		rect = (x0,y0,cellSize,cellSize)
		color = Colors.BLACK if (array[i] == True) else Colors.WHITE
		pygame.draw.rect(data.screen,color, rect,0)

def drawHelpers(data):
	x0 = 500 
	y0 = 50
	cellSize = 10
	for i in range(len(data.usedExamples)):
		x = x0 + i * cellSize * 10 + data.margin
		y = y0
		drawGridFromArray(data, data.usedExamples[i],x,y,cellSize)
		text = str(round(10 * data.usedDistance[i], 3))
		(tx, ty) = util.centerText(data.font,text, (x + x + cellSize * 10)//2, y0 + cellSize * 10 + data.margin)
		data.screen.blit(data.font.render(text, True, Colors.BLACK), (tx,ty))




def drawGridWithText(data, grid, labels):
	frame = Frame()
	frame.screen = data.screen
	frame.x = 500
	frame.y = 50
	frame.scale = 40
	for row in range(len(grid)):
		for col in range(len(grid[0])):
			x0 = util.col2X(col, frame) #inconsistant with where the x0 is offset (using frame, and inside drawrect)
			y0 = util.row2Y(row, frame)
			n = grid[row][col]
			text = str(round(n, 2))
			if row == col:
				color = Colors.GOLD
			elif n < 1:
				color = Colors.GREEN
			else:
				color = Colors.RED
			util.drawTextRect(frame, (x0, y0, frame.scale, frame.scale), data.font, text, color, Colors.BLACK)

def drawCrossVal(data):
	drawGridWithText(data, data.matrix, range(10))




##################################
## INIT STUFF
##################################




def defineGlobals(data):
	data.screenWidth = 1300
	data.screenHeight = 500
	data.usedExamples = None
	data.usedDistance = None
	data.usedLabels = None
	data.margin = 10
	data.buttonWidth = 60
	data.buttonHeight = 30
	data.grid = make2dList(10,10);
	data.gridChanged = make2dList(10,10)
	data.drawNeighbors = False
	data.showError = False
	data.buttonList = []
	data.gridCorner = (60,60);
	data.gridSize = 40	
	data.k = 5
	data.buttonDown = False
	data.usedExamples = [0] * data.k
	data.usedLabels = [0] * data.k
	data.usedDistance = [0] * data.k

	data.font = pygame.font.SysFont("monospace", 10)
	


##################################
## MAIN LOOP FUNCTIONS
##################################
def init(data):
	pygame.init()
	defineGlobals(data)
	
	screen = pygame.display.set_mode((data.screenWidth,data.screenHeight))
	data.screen = screen
			

def redraw(data):
	pygame.draw.rect(data.screen,Colors.LIGHT_GREY,(0,0,data.screenWidth,data.screenHeight),0)
	drawGrid(data)
	if data.drawNeighbors == True: drawHelpers(data)
	elif data.showError == True: drawCrossVal(data)
	pygame.display.update()
	pass


def handleEvents(data):
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			newSaveData()
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