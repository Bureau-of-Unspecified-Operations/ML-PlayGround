import numpy as np





class Layer(object):

	def __init__(self, neuron, size, prevOut):
		self.size = size
		self.neuron = neuron
		self.prevOut = prevOut
		self.weights = self.initWeights(size,prevOut)
		self.cachedOutput = None
		self.cachedSigmas = None

	def computeOutput(self):
		out = list()
		for w in self.weights:
			net = np.dot(w,prevOut)
			out.append(self.neuron.fire(net))
		return np.array(out)

	def derivativeAt(x): pass


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


	for layer in Layers:
		localDerivative = layer.neuron.derivative(layer.cachedOutput)

		if layer.type == Layer.OUTPUT:
			error = np.subtract(label, layer.cachedOutput):
			layer.cachedSigmas = -1 * np.multiply(error, localDerivative)

		elif layer.type == Layer.HIDDEN:
			error = downStreamError(layer.downLayer.cachedSigmas, layer.downLayer.weights)
			layer.cachedSigmas = np.multiply(error, localDerivative)

		elif layer.type == Layer.INPUT:
			pass

	## UPDATE WEIGHTS
	for layer in Layers:
		for w in layer.weights:
			w = w + step * np.multiply(layer.upLayer.cachedOutput, layer.cachedSigmas)



backpropagateSGD()




	