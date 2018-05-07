
import NeuralNets as nets
import jygame as jp
import pygame



class NNDrawer(object):

	def __init__(self, frame):
		self.frame = frame
		self.font = pygame.font.SysFont("monospace", 10)

	def getDrawables(self, net):
		shapes = list()
		#neuronCoords = [list()] * net.layerCount
		r = 30
		layerindex = 0
		space = self.frame.height - self.frame.margin * 2 - 4 * r # empty space between input and output layer
		layerSpacing = (space - net.layerCount * 2 * r) // (net.layerCount + 1) #could be too small and get screwed

		curLayer = net.inputLayer

		while curLayer != None:
			
			if curLayer.type == nets.Layer.OUTPUT:
				y = self.frame.margin + r
			elif curLayer.type == nets.Layer.INPUT:
				y = self.frame.height - self.frame.margin - r
			else: y = self.frame.margin + r + (layerindex + 1) * (layerSpacing + 2 * r)

			neuronSpacing = (self.frame.width - curLayer.nCount * 2 * r) // (curLayer.nCount + 1)
			if(neuronSpacing < 2 * r): print("too small")

			xB = 0 - r # makes future spacing consistant
			for i in range(curLayer.nCount):
				x = xB + (1 + i) * (neuronSpacing + 2 * r) 
				#neuronCoords[layerindex].append((x,y)) # picture this as upside down!!
				print("neruons at (" + str(x) + "," + str(y) + ")" )
				shapes.append(self.createNeuron((x,y,r), curLayer.neuron, curLayer.cachedOutput[i]))

			layerindex += 1
			curLayer = curLayer.downLayer

		return shapes


	def createNeuron(self,circle, neuron, output):
		rgb = jp.util.rescale(output, neuron.lo, neuron.hi, 0, 255)
		color = (rgb, rgb, rgb)
		text = neuron.text
		(cx, cy, cr) = circle
		(tx, ty) = jp.util.centerText(self.font,text, cx, cy);
		return jp.DrawableTextCircle(cx, cy, cr, tx, ty, self.font, text, color)


	def mouseEvent(self, x, y, type):
		pass


