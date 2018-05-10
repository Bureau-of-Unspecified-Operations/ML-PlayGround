
import NeuralNets as nets
import Neurons
import jygame as jp
import pygame
import Colors
import TrainingViewModel as TVM




class NNDrawer(object):

	def __init__(self, frame):
		self.frame = frame
		self.net = nets.NetEditor.newNet(100, 10, Neurons.Sigmoid(), nets.Net.leastSquaredDerivative,(Neurons.Sigmoid(), 2))
		self.buttons = list()
		self.font = pygame.font.SysFont("arial", 10)



	def getDrawables(self):
		shapes = list()
		shapes.extend(self.drawablesFromNet(self.net))
		shapes.extend(self.buttons)
		return shapes


	def createNeuron(self,circle, neuron, output):
		rgb = jp.util.rescale(output, neuron.lo, neuron.hi, 0, 255)
		color = (rgb, rgb, rgb)
		text = neuron.text
		(cx, cy, cr) = circle
		(tx, ty) = jp.util.centerText(self.font,text, cx, cy);
		return jp.DrawableTextCircle(cx, cy, cr, tx, ty, self.font, text, color)

	def makeLines(self,weights, point, points, r):
		# print("len of weights " + str(len(weights)))
		# print("len of points " + str(len(points)))
		# print(points)
		##assert(len(weights) == len(points))
		##WILL BE ADDING SHIT WHEN YOU ACTUALLY USE WEIGHTS
		shapes = list()
		for i in range(len(points)):
			(x1, y1) = point
			(x2, y2) = points[i]
			shapes.append(jp.DrawableLine((x1, y1 + r), (x2, y2 - r), 3, Colors.RED))
		return shapes


	def mouseEvent(self, x, y, eventType):
		if eventType == pygame.MOUSEBUTTONDOWN:
			for button in self.buttons:
				if button.inRange(x,y):
					button.onClick()
		pass

	def quit(self):
		pass

	def drawablesFromNet(self, net):
		lc = net.layerCount()
		del self.buttons[:]
		shapes = list()
		neuronCoords = [list() for i in range(lc)]
		r = 30
		layerindex = 0

		space = self.frame.height - self.frame.margin * 2 - 4 * r # empty space between input and output layer
		#print("space " + str(space))
		layerSpacing = (space - (lc - 2) * 2 * r) // (lc - 1) #could be too small and get screwed
		#print("layerspacing " + str(layerSpacing))
		

		curLayer = net.inputLayer

		while curLayer != None:
			# print("index " + str(layerindex))
			# print("layer type " + str(curLayer.type))
			if curLayer.type == nets.Layer.OUTPUT:
				y = self.frame.margin + r
			elif curLayer.type == nets.Layer.INPUT:
				y = self.frame.height - self.frame.margin - r
			else: y = self.frame.height - (self.frame.margin + r + (layerindex) * (layerSpacing + 2 * r)) #goes from the bottom up
			#print("y " + str(y) + "  index amount " + str((layerindex + 1) * (layerSpacing + 2 * r)))


			

			#print("ncount str " + str(curLayer.nCount))
			neuronSpacing = (self.frame.width - curLayer.nCount * 2 * r) // (curLayer.nCount + 1)
			#print("ncount post str " + str(curLayer.nCount))
			#print("neuron  spacing " + str(neuronSpacing))
			minxSpacing = 100
			maxNeurons = (self.frame.width - minxSpacing) // (minxSpacing + 2 * r)
			#print("max neuron " + str(maxNeurons))
			if(neuronSpacing < minxSpacing):
				x0 = 0
				xB = 0 - r
				for i in range(maxNeurons):
					if i == maxNeurons // 2:
						x = xB + (1 + i) * (minxSpacing + 2 * r)
						shapes.extend(jp.util.dotdotdot(r//3, x, y, r))
					else:
						x = xB + (1 + i) * (minxSpacing + 2 * r)
						if i == 0: x0 = x
						j = self.collapsedIndex(curLayer.nCount, maxNeurons, i) 
						# print("i " + str(i))
						# print("j " + str(j))
						# print("index " + str(layerindex))
						# print(curLayer.weights)
						neuronCoords[layerindex].append((x,y)) # picture this as upside down!!
						shapes.append(self.createNeuron((x,y,r), curLayer.neuron, curLayer.cachedOutput[j]))
						if curLayer.upLayer != None:

							shapes.extend(self.makeLines(curLayer.weights[:,i], (x,y), neuronCoords[layerindex - 1], r))
			else:
				x0 = 0
				xB = 0 - r # makes future spacing consistant
				for i in range(curLayer.nCount):
					# print("i " + str(i))
					# print("ind " + str(layerindex))
					x = xB + (1 + i) * (neuronSpacing + 2 * r) 
					if i == 0: x0 = x
					#print(neuronCoords)
					neuronCoords[layerindex].append((x,y)) # picture this as upside down!!
					shapes.append(self.createNeuron((x,y,r), curLayer.neuron, curLayer.cachedOutput[i]))
					if curLayer.upLayer != None:
						shapes.extend(self.makeLines(curLayer.weights[:,i],(x,y),neuronCoords[layerindex - 1],r))

			if(curLayer.type != nets.Layer.INPUT and curLayer.type != nets.Layer.OUTPUT):
				self.buttons.append(DeleteLayer(curLayer, (x0 - self.frame.margin * 10, y)))
				self.buttons.append(EditNeuron(curLayer, (x + self.frame.margin * 10, y), 1, None))
				self.buttons.append(EditNeuron(curLayer, (x + self.frame.margin * 13, y), -1, None))
			if curLayer.type != nets.Layer.INPUT:
				xm = x0 - self.frame.margin * 10
				ym = y + layerSpacing // 2
				self.buttons.append(AddLayer(curLayer.upLayer, curLayer,(xm,ym)))

			
			#print(neuronCoords)
			layerindex += 1
			curLayer = curLayer.downLayer


		# for i,buttonLayer in enumerate(neuronCoords):
		# 	if

		return shapes

	def collapsedIndex(self, realCnt, visCnt, i):
		if i < visCnt // 2:
			return i
		elif i > visCnt // 2:
			return realCnt - visCnt + i

		else: print("error in collapsed")



class DeleteLayer(object):

	def __init__(self, layer, coord):
		self.layer = layer
		(self.x, self.y) = coord
		self.r = 10
		self.color = Colors.SILVER

	def draw(self, frame):
		pygame.draw.circle(frame.screen, self.color, (self.x, self.y), self.r)

	def onClick(self):
		nets.NetEditor.spliceOut(self.layer)

	def inRange(self, x, y):
		return jp.util.inCircleRange(x, y, self.x, self.y, self.r)

class AddLayer(DeleteLayer):

	def __init__(self, upLayer, downLayer, coord):
		self.upLayer = upLayer
		self.downLayer = downLayer
		(self.x, self.y) = coord
		self.r = 10
		self.color = Colors.ORANGE

	def onClick(self):
		layer = nets.Layer(Neurons.Sigmoid, 3, nets.Layer.HIDDEN)
		nets.NetEditor.spliceIn(layer,self.upLayer, self.downLayer)

class EditNeuron(DeleteLayer):
	def __init__(self, layer, coord, op, neuron):
		super().__init__(layer, coord)
		self.op = op
		self.neuron = neuron

	def onClick(self):
		nets.NetEditor.editNode(self.layer, self.op, self.neuron)





