import numpy as np





class Layer(object):

	def __init__(self, neuron, downLayer, upLayer, size, typein):
		self.neuron = neuron
		self.upLayer = upLayer
		self.downLayer = downLayer
		self.weights = weights
		self.type = type
		self.cachedOutput = np.zeros(size)
		self.cachedSigmas = np.zeros(size)

	def compute(self):
		out = list()
		for w in self.weights:
			net = np.dot(w, self.upLayer.cachedOutput)
			out.append(self.neuron.fire(net))
		self.cachedOutput = np.array(out)
		return self.cachedOutput

class HiddenLayer(Layer):

class OutputLayer(Layer):
	def __init__(self, neuron, upLayer, size):
		super().__init__(neuron, None, upLayer, size, Layer.OUTPUT)

class InputLayer(Layer):
	def __init__(self, downLayer, size):
		super().__init__(self, None, downLayer, None, size, Layer.INPUT)


class NeuralNet(object):

	def __init__(self):
		self.inputLayer
		self.outputLayer
		self.layers


	def compute(self, example):
		self.inputLayer.cachedOutput = example
		layer = self.inputLayer.downLayer
		while(layer.type != Layer.OUTPUT):
			layer.compute()
			layer = layer.downLayer
		return layer.compute




# destructively modifies net to update weights.
def backpropagateSGD(data, step, net):
	def downStreamError(sigmas,weights):
		# assert len(sigmas) == len(wieghts)
		errorArray = np.zeros(len(weights[0]))
		for i, w in enumerate(weights):
			errorArray = np.add(errorArray, sigmas[i] * w)
		return errorArray

	(ex, label) = data
	net.cachedCompute(ex);
	layer = net.outputLayer

	while layer.type != Layer.INPUT:
		localDerivative = layer.neuron.derivative(layer.cachedOutput)
		error = np.zeros(len(localDerivative))  
		if layer.type == Layer.OUTPUT:
			error = np.subtract(label, layer.cachedOutput):
		elif layer.type == Layer.HIDDEN:
			error = downStreamError(layer.downLayer.cachedSigmas, layer.downLayer.weights)
		layer.cachedSigmas = -1 * np.multiply(error, localDerivative)
		layer = layer.upLayer



	## UPDATE WEIGHTS
	layer = net.outputLayer
	while layer.type != INPUT:
		for w in layer.weights:
			w = w + step * np.multiply(layer.upLayer.cachedOutput, layer.cachedSigmas)
		layer = layer.upLayer



backpropagateSGD()




	