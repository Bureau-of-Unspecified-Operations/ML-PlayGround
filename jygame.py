import pygame
import math
import Colors



class util(object):
	

	def dist(p0, p1):
		assert(len(p0) == len(p1))
		s = 0
		for i in range(len(p0)):
			s += (p0[i] - p1[i]) ** 2
		return math.sqrt(s)

	def inCircleRange(x0, y0, x1, y1, r):
		return util.dist((x0,y0),(x1,y1)) <= r

	def inRectRange(x0, y0, rx, ry, rw, rh):
		return (x0 <= rx + rw and x0 > rx and
			   y0 <= ry + rh and y0 > ry)

	def centerText(font, text, x, y):
		width, height = font.size(text)
		x0 = x - width // 2
		y0 = y - height // 2
		return (x0, y0)

	def row2Y(row, frame):
		return frame.y + row * frame.scale
	def col2X(col, frame):
		return frame.x + col * frame.scale
	def x2Col(x, frame):
		return (x - frame.x) // frame.scale
	def y2Row(y, frame):
		return (y - frame.y) // frame.scale



	def drawTextRect(frame, rect, font, text, rColor, tColor):
		(x, y, width, height) = rect
		pygame.draw.rect(frame.screen, rColor, rect, 0);
		cx = (x + x + width) // 2  #error with median
		cy = (y + y + height) // 2
		(tx, ty) = util.centerText(font, text, cx, cy)
		#print("X: %d, y: %d, tx: %d, ty: %d, cx: %d, cy: %d"%(x,y,tx,ty,cx,cy))
		frame.screen.blit(font.render(text, True, tColor), (tx, ty))


	#best for scalling up (cause integer division)
	def rescale(x, lo0, hi0, lo1, hi1):
		return (x * (hi1-lo1) - lo1 * hi0 - lo0 * hi1) // (hi0 - lo0)

	def dotdotdot(rD, x, y, space):
		shapes = list()
		for i in range(3):
			cx = x - space - 2 * rD + i * (space + 2 * rD)
			cy = y
			shapes.append(DrawableCircle(cx, cy, rD, Colors.WHITE))
		return shapes

	###########################################3333
	## GRID STUFF
	#############################333

	def row2Y(row, size, y0):
		return y0 + row * size
	def col2X(col, size, x0):
		return x0 + col * size
	def x2Col(x, size, x0):
		return (x - x0) // size
	def y2Row(y, size, y0):
		return (y - y0) // size

	def make2dList(rows, cols):
		a = []
		for row in range(rows):
			a.append([False] * cols);
		return a

	# destructive
	def fill2dList(l,val):
		for row in range(len(l)):
			for col in range(len(l[0])): #bitches!!
				l[row][col] = val

	def inBounds(row, col, x, y, cellSize, x0, y0):
		x0 = util.col2X(col, cellSize, x0)
		y0 = util.row2Y(row, cellSize, y0)
		return (x0 <= x and x <= x0 + cellSize and
				y0 <= y and y <= y0 + cellSize)

	#####33333333333###############################3


##########################################
## DRAWABLES
#######################################

class DrawableCircle(object):
	def __init__(self,cx,cy,cr, color):
		self.cx = cx
		self.cy = cy
		self.cr = cr
		self.color = color

	def draw(self, frame):
		pygame.draw.circle(frame.screen, self.color, (self.cx, self.cy), self.cr)
	

class DrawableTextCircle(object):
	def __init__(self,cx,cy,cr,tx,ty,font,text,color):
		self.cx = cx
		self.cy = cy
		self.cr = cr
		self.tx = tx
		self.ty = ty
		self.font = font
		self.text = text
		self.color = color

	def draw(self, frame):
		pygame.draw.circle(frame.screen, self.color, (self.cx, self.cy), self.cr)
		frame.screen.blit(self.font.render(self.text, True, Colors.ORANGE), (self.tx, self.ty));

class DrawableLine(object):
	def __init__(self, start, end, thickness, color):
		self.start = start
		self.end = end
		self.thickness = thickness;
		self.color = color

	def draw(self, frame):
		pygame.draw.line(frame.screen, self.color, self.start, self.end, self.thickness)



class DrawableGrid(object):
	def __init__(self, array, x, y, cellSize):
		self.grid = array
		self.cellSize = cellSize
		self.x = x
		self.y = y

	def draw(self, frame):
		for row in range(len(self.grid)):
			for col in range(len(self.grid[0])):
				color = Colors.BLACK if (self.grid[row][col] == True) else Colors.WHITE
				rect = (util.col2X(col, self.cellSize, self.x), util.row2Y(row, self.cellSize, self.y), self.cellSize, self.cellSize)
				pygame.draw.rect(frame.screen,color, rect,0)




class FrequencyTable(object):
	def __init__(self, freqTable, x, y, spacing):
		self.freqTable = freqTable
		self.x = x
		self.y = y
		self.spacing = spacing
		self.font = pygame.font.SysFont("monospace", 10)

	def draw(self, frame):
		for i, key in enumerate(self.freqTable.keys()):
			text = str(key) + ": " + str(self.freqTable[key]) + " instances"
			x = self.x
			y = self.y + i * self.spacing
			frame.screen.blit(self.font.render(text, True, Colors.BLACK), (x, y))
####################3
## BUTTONS
####################

class TestButton(object):

	def __init__(self):
		pass

	def onClick(self):
		self.buttons.extend(self.dataModel.getTestButtons())
		self.shapes.extend(self.dataModel.getTestDrawables())



class GenericRectButton(object):
	def __init__(self, function, text, rect):
		self.function = function
		self.text = text
		self.rect = rect
		self.color = Colors.SILVER
		self.font = pygame.font.SysFont("monospace", 15)
		(self.tx, self.ty) = util.centerText(self.font, self.text, self.rect[0] + self.rect[2] // 2, self.rect[1] + rect[3] // 2) 

	def onClick(self):
		self.function()

	def draw(self, frame):
		print("hello")
		pygame.draw.rect(frame.screen, self.color, self.rect)
		frame.screen.blit(self.font.render(self.text, True, Colors.ORANGE), (self.tx, self.ty));

	def inRange(self, x, y):
		(rx, ry, rw, rh) = self.rect
		return util.inRectRange(x, y, rx, ry, rw, rh)


#################################################33

class Frame(object):
	def __init__(self, coord, width, height):
		(self.x, self.y) = coord
		self.width = width
		self.height = height
		self.screen = pygame.Surface((width, height))


	def containsCoord(self, x, y):
		return x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height

	def transform(self, x, y):
		x0 = x - self.x
		y0 = y - self.y
		return (x0, y0)



