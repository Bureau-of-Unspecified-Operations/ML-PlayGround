
import NeuralNets as nets
import jygame as jy



def NNDrawer(object):

	def __init__(self, frame, net):
		self.x0 = frame.x0
		self.y0 = frame.y0
		self.width = frame.width
		self.height = frame.height
		self.net
		self.font = pygame.font.SysFont("monospace", 10)


	


	def update(self):
		shapes = list()
		layerindex = 0
		space = self.height - self.margin * 2 - 4 * r # empty space between input and output layer
		layerSpacing = (space - self.net.layerCount * 2 * r) // (self.net.layerCount + 1) #could be too small and get screwed

		while layer != nets.Layer.INPUT:
			
			if layer.type == nets.Layer.OUTPUT:
				y = self.y0 + self.margin + r
			elif layer.type == nets.Layer.INPUT:
				y = self.y0 + self.height - self.margin -r
			else: y = self.y0 + self.margin + r + (layerindex + 1) * (layerSpacing + 2 * r)

			neuronSpacing = (self.width - nCount * 2 * r) // (nCount + 1)
			if(neuronSpacing < 2 * r): print("too small")

			xB = self.x0 - r #makes future spacing consistant
			for i in range(len(layer.nCount)):
				x = xB + (1 + i) * (neuronSpacing + 2 * r) 
				shapes.append(createNeuron((x,y,r), neuron, layer.cachedOutputs[i]))

			layerindex += 1

		return shapes


	def createNeuron(self,circle, neuron, output):
		rgb = jp.rescale(output, neuron.lo, neuron.hi, 0, 255)
		color = (rgb, rgb, rgb)
		text = neuron.text
		(cx, cy, cr) = circle
		(tx, ty) = jy.util.centerText(font,text, cx, cy);
		return DrawableNeuron(frame, cx, cy, cr, tx, ty, self.font, text, color)




