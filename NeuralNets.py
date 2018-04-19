import numpy as np
import Neurons





class Layer(object):
	HIDDEN = 0
	INPUT = 1
	OUTPUT = 2
	#giving weights should really wait till later
	def __init__(self, neuron, downLayer, upLayer, nCount,wSize, typein):
		self.neuron = neuron
		self.upLayer = upLayer
		self.downLayer = downLayer
		self.weights = [np.zeros(wSize)] * nCount
		self.type = typein
		self.cachedOutput = np.zeros(nCount)
		self.cachedSigmas = np.zeros(nCount)

	def compute(self):
		out = list()
		for w in self.weights:
			net = np.dot(w, self.upLayer.cachedOutput)
			out.append(self.neuron.fire(net))
		self.cachedOutput = np.array(out)
		return self.cachedOutput


class HiddenLayer(Layer):
	def __init__(self, neuron, downLayer, upLayer, nCount, wSize):
		super().__init__(neuron, downLayer, upLayer, nCount, wSize, Layer.HIDDEN)

class OutputLayer(Layer):
	def __init__(self, neuron, upLayer, nCount, wSize):
		super().__init__(neuron, None, upLayer, nCount, wSize, Layer.OUTPUT)

class InputLayer(Layer):
	def __init__(self, downLayer, nCount, wSize):
		super().__init__(None, downLayer, None, nCount, wSize, Layer.INPUT)

class SoftMaxLayer(Layer):
	def compute(self):
		for w in self.weights:
			net = np.dot(w, self.upLayer.cachedOutput)
			out.append(self.neuron.fire)


class Net(object):

	def __init__(self,inSize,hSize,oSize):
		self.inputLayer = InputLayer(None, inSize, inSize)
		self.hiddenLayer = HiddenLayer(Neurons.Sigmoid(), None, None, hSize, hSize)  ### hacky shit TO REMOVE
		self.outputLayer = OutputLayer(Neurons.Sigmoid(), None, oSize, hSize)
		self.connect(self.inputLayer, self.hiddenLayer)
		self.connect(self.hiddenLayer, self.outputLayer)


	def compute(self, example):
		self.inputLayer.cachedOutput = example
		layer = self.inputLayer.downLayer
		while(layer.type != Layer.OUTPUT):
			layer.compute()
			layer = layer.downLayer
		return layer.compute

	def connect(self, upLayer, downLayer):
		upLayer.downLayer = downLayer
		downLayer.upLayer = upLayer

	def train(data, labels):
		# assert len(data) == len(labels)
		for i in range(len(data)):
			backpropagateSGD(data[i],labels[i], self.step, self)



def softMaxBackProp():

	while layer.type != Layer.INPUT:
		if layer.type == Layer.OUTPUT:
			error = layer.cachedOutput[trueIndex]
			derivate = layer.neuron.derivative(layer.cachedOutput, trueIndex)
		elif layer.type == Layer.HIDDEN:
			error = 


# destructively modifies net to update weights.
def backpropagateSGD(example, label step, net):
	def downStreamError(sigmas,weights):
		# assert len(sigmas) == len(wieghts)
		errorArray = np.zeros(len(weights[0]))
		for i, w in enumerate(weights):
			errorArray = np.add(errorArray, sigmas[i] * w)
		return errorArray

	net.compute(example);
	layer = net.outputLayer

	while layer.type != Layer.INPUT:
		derivative = np.vectorize(layer.neuron.derivative())
		localDerivative = derivative(layer.cachedOutput)
		error = np.zeros(len(localDerivative))  
		if layer.type == Layer.OUTPUT:
			error = np.subtract(label, layer.cachedOutput)
		elif layer.type == Layer.HIDDEN:
			error = downStreamError(layer.downLayer.cachedSigmas, layer.downLayer.weights)
		layer.cachedSigmas = -1 * np.multiply(error, localDerivative)
		layer = layer.upLayer

	## UPDATE WEIGHTS
	layer = net.outputLayer
	while layer.type != Layer.INPUT:
		for w in layer.weights:
			w = w + step * np.multiply(layer.upLayer.cachedOutput, layer.cachedSigmas)
		layer = layer.upLayer



net = Net(2,2,2)
print(net)
data = (np.full(2,1), np.full(2,5))
backpropagateSGD(data, 1, net)




	