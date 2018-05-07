import numpy as np
import Neurons







class Layer(object):
	HIDDEN = 0
	INPUT = 1
	OUTPUT = 2
	#giving weights should really wait till later
	def __init__(self, neuron, nCount, typein):
		self.neuron = neuron
		self.upLayer = None
		self.downLayer = None
		self.weights = None
		self.type = typein
		self.cachedOutput = np.zeros(nCount)
		self.cachedSigmas = np.zeros(nCount)
		self.nCount = nCount

	def compute(self):
		nets = list()
		for w in self.weights:
			nets.append(np.dot(w, self.upLayer.cachedOutput))
		self.cachedOutput = self.neuron.fire(np.array(nets))
		return self.cachedOutput

	def setWeights(self, n):
		self.weights = [np.zeros(n)] * self.nCount  #make all array for effic

"""
class HiddenLayer(Layer):
	def __init__(self, neuron, nCount):
		super().__init__(neuron, nCount, Layer.HIDDEN)

class OutputLayer(Layer):
	def __init__(self, neuron, nCount):
		super().__init__(neuron, nCount, Layer.OUTPUT)

class InputLayer(Layer):
	def __init__(self, nCount):
		super().__init__(None, nCount, Layer.INPUT)
"""

class Net(object):
	# args should be a list of (neuron, nCount) pairs describing the hidden layers you want
	def __init__(self, inputSize, outputSize, outputNeuron, lossDerivative, *args):
		self.inputLayer = Layer(Neurons.Blank, inputSize, Layer.INPUT)
		self.outputLayer = Layer(outputNeuron, outputSize, Layer.OUTPUT)
		self.lossDerivative = lossDerivative
		hiddenLayer = None
		upLayer = self.inputLayer
		for i in range(len(args)):
			hiddenLayer = Layer(args[i][0],args[i][1], Layer.HIDDEN)
			self.connect(upLayer, hiddenLayer);
		self.connect(hiddenLayer, self.outputLayer)
		self.layerCount = 2 + len(args)


	def compute(self, example):
		self.inputLayer.cachedOutput = example
		layer = self.inputLayer.downLayer # handles how input works
		while(layer.type != Layer.OUTPUT):
			layer.compute()
			layer = layer.downLayer
		return layer.compute()


	def connect(self, upLayer, downLayer):
		upLayer.downLayer = downLayer
		downLayer.upLayer = upLayer
		downLayer.setWeights(upLayer.nCount)

	def train(self, data, labels):
		# assert len(data) == len(labels)
		for i in range(len(data)):
			backpropagateSGD(data[i],labels[i], self.step, self)

	def backpropagateSGD(self, example, label, step):
		def downStreamError(sigmas, weights):
			## assert len(sigmas) == len(weights)
			# COULD ELIMINATE FOR LOOP?
			errorArr = np.zeros(len(weights))
			for i, w in enumerate(weights):
				# the weights for each node "stack" on top of each other
				# multiplied by the sigma of that node
				errorArr = np.add(errorArr, sigmas[i] * w)
			return errorArr

		# propagate example through net
		self.compute(example)
		layer = self.outputLayer

		# Caclulate the deltas
		while layer.type != Layer.INPUT:
			error = None
			## Non-softmax layers won't need the lable, but they get it anyways
			localDerivative = layer.neuron.derivative(layer.cachedOutput, label)
			if layer.type == Layer.OUTPUT:
				error = self.lossDerivative(layer.cachedOutput, label);
			elif layer.type == Layer.HIDDEN:
				error = downStreamError(layer.downLayer.cachedSigmas,layer.downLayer.weights)

			layer.cachedSigmas = np.multiply(error, localDerivative)
			layer = layer.upLayer

		# Update Weights
		layer = self.outputLayer
		while layer.type != Layer.INPUT:
			for i, w in enumerate(layer.weights):
				w = w + (-1) * step * layer.upLayer.cachedOutput * layer.cachedSigmas[i]
			layer = layer.upLayer


	def crossEntropy(layer,label):
		index = -1
		for i in range(len(label)):
			if label[i] == 1: index = i 
		assert(index != -1)
		return -1 / layer[index]

	def leastSquaredDerivative(output, label):
		assert(len(output) == len(label))
		error = np.subtract(output,label)
		return error

	def adapterCompute(self, example):
		results = self.compute(example)
		return np.argmax(results)

	def train(self, data, labels):
		step = .3
		maxIter = 1
		for t in range(maxIter):
			for i, example in enumerate(data):
				self.backpropagateSGD(example, labels[i], step)









"""
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
"""







	