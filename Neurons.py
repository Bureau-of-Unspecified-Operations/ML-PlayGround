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


		
