import math
import numpy as np

class Sigmoid(object):
	def fire(self, netArr):
		def func(x):
			return 1 / (1 + math.exp(-x))
		vectorized = np.vectorize(func)
		return vectorized(netArr)

	def derivative(self, netArr, label):
		return np.multiply(netArr, 1 - netArr)
		

class Softmax(object):
	def fire(self, netArr):
		def func(x):
			return math.exp(x)
		vectorFun = np.vectorize(func)
		netArr = vectorFun(netArr)
		norm = np.sum(netArr)
		netArr = netArr / norm
		return netArr
	def derivative(self, softOut, label):
		index = -1
		for i in range(len(label)):
			if label[i] == 1: index = i
		assert(index != -1)
		arr = np.zeros(len(softOut))
		for i in range(len(arr)):
			arr[i] = 1 - softOut[i] if i == index else -softOut[i]
		return softOut[index] * arr		

class Perceptron(object):
	def fire(self, net):
		return 0 if net < 0 else 1
	def derivativeAt(x):
		raise ValueError("oops, perceptron doesn't have a derivative")

class Tanh(object):
	def fire(self, net):
		o = (math.exp(net) - math.exp(-net)) / (math.exp(net) + math.exp(-net))
		return o

	def derivativeAt(self, x):
		return 1 - self.fire(x) ** 2

class Linear(object):
	def fire(self, net):
		return net

	def derivativeAt(self, x):
		return 1


		
