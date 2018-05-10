from random import shuffle
import numpy as np


class TestTrainModel(object):

	def __init__(self, algo, drawer, data):
		self.algo = algo
		self.drawer = drawer
		self.data = data

	def testOnSingle(self):
		vector = self.drawer.getVector()
		pred = self.algo.classify(vector)
		return pred


	def train(self):
		curData = self.data.workingset
		self.algo.train(curData)
		print("finished training")


	def crossWrapper(self):
		foldsize = len(self.data.workingset) // 10
		return self.crossValidate(foldsize, self.data.workingset)

	def crossValidate(self, foldSize, data):
		#randomize examples and labels
		shuffle(data)
		errSum = 0
		k = len(data) // foldSize
		averageMatrix = np.zeros((10,10))
		for start in range(k):
			test = data[start:start + foldSize]
			training = data[0:start] + data[start + foldSize:len(data)]
			matrix = self.predMatrix(training, test)
			#print(matrix)
			error = self.matrix2Error(matrix, foldSize)
			print("partial err= %d"%(error))
			errSum += error
			averageMatrix = np.add(averageMatrix, matrix)

		error = errSum / k
		#errorMatrix = averageMatrix / k
		return (error, averageMatrix)

	#pred matrix from a signle pass on testData, trained on the training data
	def predMatrix(self, trainingData, testData):
		predMatrix = np.zeros((10,10))		
		for point in testData:
			(example, label) = point
			self.algo.train(trainingData)
			(ans, metaData) = self.algo.classify(example)
			predMatrix[label][ans] += 1
		return predMatrix


	def matrix2Error(self, matrix, total):
		correct = 0
		for i in range(len(matrix)):
			correct += matrix[i][i]
		return correct / total