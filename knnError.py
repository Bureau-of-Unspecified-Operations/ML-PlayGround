import KNN
from random import shuffle
import numpy as np

def make2dList(rows, cols, value):
	a = []
	for row in range(rows):
		a.append([value] * cols);
	return a

class KNNTester(object):

	def __init__(self, knn):
		self.knn = knn

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


	def predMatrix(self, trainingData, testData):
		predMatrix = np.zeros((10,10))		
		for point in testData:
			(example, label) = point
			(ans, metaData) = self.knn.classify(trainingData, example)
			predMatrix[label][ans] += 1
		return predMatrix


	def matrix2Error(self, matrix, total):
		correct = 0
		for i in range(len(matrix)):
			correct += matrix[i][i]
		return correct / total
