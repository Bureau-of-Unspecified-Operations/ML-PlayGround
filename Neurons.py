import math
import numpy as np

class Sigmoid(object):
	def fire(self, net):
		o = 1 / (1 + math.exp(-net))
		return o

	def derivative(self):
		def myDerivative(x):
			return np.multiply(x, 1 - x)
		return myDerivative;

class Softmax(object):
	def fire(self, netArr):
		def func(x):
			return math.exp(x)
		vectorFun = np.vectorize(func)
		netArr = vectorFun(netArr)
		norm = np.sum(netArr)
		netArr = netArr / norm
		return netArr
	def derivative(self, softOut, trueIndex):
		arr = np.zeros(len(softOut))
		for i in range(len(arr)):
			arr[i] = 1 - softOut[i] if i == trueIndex else -softOut[i]
		return softOut[trueIndex] * arr
		

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


		
