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
		dot = np.dot(self.upLayer.cachedOutput, self.weights)
		self.cachedOutput = self.neuron.fire(dot)
		return self.cachedOutput

	# weight vectors are NxM, n is cnt in last (# of indexes), M is neurons in cur layer (# of wights)
	def setWeights(self, n):
		self.weights = np.full((n, self.nCount), 0.1)


class Net(object):
	def __init__(self, inputLayer, outputLayer, lossDerivative):
		self.inputLayer = inputLayer
		self.outputLayer = outputLayer
		self.lossDerivative = lossDerivative
	

	def layerCount(self):
		cnt = 0
		layer = self.inputLayer
		while layer != None:
			cnt += 1
			layer = layer.downLayer
		return cnt


	def compute(self, example):
		self.inputLayer.cachedOutput = np.array(example)
		layer = self.inputLayer.downLayer # handles how input works
		while(layer.type != Layer.OUTPUT):
			layer.compute()
			layer = layer.downLayer
		return layer.compute()

	def classify(self, vector):
		pred = self.compute(vector)
		print("did a classify")
		return np.argmax(pred)


	def connect(self, upLayer, downLayer):
		upLayer.downLayer = downLayer
		downLayer.upLayer = upLayer
		downLayer.setWeights(upLayer.nCount)


	def backpropagateSGD(self, example, label, step):

		def downStreamError(sigmas, weights):
			# the weights for each node "stack" on top of each other
			# multiplied by the sigma of that node
			# print("weights")
			# print(weights)
			# print("sigms")
			# print(sigmas)
			err = np.multiply(weights, sigmas)
			tmp = np.sum(err, axis=1)
			# print("weights post")
			# print(err)
			return 	tmp		

		# propagate example through net
		self.compute(example)
		layer = self.outputLayer

		cnt = 0
		# Caclulate the deltas
		while layer.type != Layer.INPUT:
			error = None
			## Non-softmax layers won't need the lable, but they get it anyways
			localDerivative = layer.neuron.derivative(layer.cachedOutput, label)
			if layer.type == Layer.OUTPUT:
				error = self.lossDerivative(layer.cachedOutput, label);
			elif layer.type == Layer.HIDDEN:
				error = downStreamError(layer.downLayer.cachedSigmas,layer.downLayer.weights)

			# print("layer " + str(cnt))
			# print("error")
			# print(error)
			# print("deriv")
			# print(localDerivative)

			layer.cachedSigmas = np.multiply(error, localDerivative)
			# print("sigmas ")
			# print(layer.cachedSigmas)
			# print("layer done \n")
			layer = layer.upLayer
			cnt +=1

		# Update Weights
		layer = self.outputLayer
		while layer.type != Layer.INPUT:
			cache = layer.upLayer.cachedOutput
			transCache = cache.reshape(cache.shape[0],-1) # squash into column vector
			temp = np.multiply(layer.weights, transCache)  # mult each index (row) by relevant output
			temp = np.multiply(temp, layer.cachedSigmas) # mult each weight (col) by relevant sigma
			layer.weights = layer.weights + temp * (-1) * step 
			layer = layer.upLayer


	def crossEntropyDerivative(layer,label):
		index = np.argmax(label)
		temp = np.zeros(len(layer))
		temp[index] = -1 / layer[index]
		return temp

	def leastSquaredDerivative(output, label):
		assert(len(output) == len(label))
		error = np.subtract(output,label)
		return error

	def adapterCompute(self, example):
		results = self.compute(example)
		return np.argmax(results)

	def adapter(self, label):
		arr = np.zeros(10)
		arr[int(label)] = 1
		return arr

	def train(self, trainingData):
		print("trained")
		step = .01
		maxIter = 20
		for t in range(maxIter):
			for i in range(len(trainingData)):
				example = trainingData[i][0]
				#print(example)
				label = self.adapter(trainingData[i][1])
				#print(label)
				self.backpropagateSGD(example, label, step)
		#self.printSigmas()
		#self.printWeights()

	def printWeights(self):
		layer = self.inputLayer
		cnt = 0
		while layer != None:
			print("layer " + str(cnt))
			print(layer.weights)
			cnt += 1
			layer = layer.downLayer

	def printSigmas(self):
		layer = self.inputLayer
		cnt = 0
		while layer != None:
			print("layer " + str(cnt))
			print(layer.cachedSigmas)
			cnt += 1
			layer = layer.downLayer



class NetEditor(object):

	def connect(upLayer, downLayer):
		upLayer.downLayer = downLayer
		downLayer.upLayer = upLayer
		downLayer.setWeights(upLayer.nCount)

	def spliceOut(layer):
		if layer.upLayer != None and layer.downLayer != None:
			NetEditor.connect(layer.upLayer, layer.downLayer);
		else: print("can't splice out, there aren't layers on either side")

	def spliceIn(layer, upLayer, downLayer):
		NetEditor.connect(upLayer, layer)
		NetEditor.connect(layer, downLayer);


		#not safe for end layers
	def editNode(layer, op, neuron):
		layer.nCount += op
		if(neuron != None): layer.neuron = neuron
		if op != 0:
			layer.cachedOutput = np.zeros(layer.nCount)
			layer.cachedSigmas = np.zeros(layer.nCount)
			cntUpper = layer.upLayer.nCount
			layer.setWeights(cntUpper)
			layer.downLayer.setWeights(layer.nCount)

	#net Constructor
	def newNet(inputSize, outputSize, outputNeuron, lossDerivative, *args):
		inputLayer = Layer(Neurons.Blank, inputSize, Layer.INPUT)
		outputLayer = Layer(outputNeuron, outputSize, Layer.OUTPUT)
		hiddenLayer = None
		upLayer = inputLayer
		for i in range(len(args)):
			hiddenLayer = Layer(args[i][0],args[i][1], Layer.HIDDEN)
			NetEditor.connect(upLayer, hiddenLayer);
			upLayer = hiddenLayer
		NetEditor.connect(hiddenLayer, outputLayer)
		
		return Net(inputLayer, outputLayer, lossDerivative)







	















	