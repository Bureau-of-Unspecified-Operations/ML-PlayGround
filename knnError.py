import KNN

def make2dList(rows, cols, value):
	a = []
	for row in range(rows):
		a.append([value] * cols);
	return a

def KNNTester(object):

	def __init__(self, examples, labels):
		self.examples = examples
		self.labels = labels
		self.data = [(examples[i],labels[i]) for i in range(len(examples))]

	def crossValidate(foldSize, data):
		#randomize examples and labels
		data.shuffle()
		errSum = 0
		k = len(data) // foldSize
		for start in range(k):
			test = examples[start:start + foldSize]
			training = examples[0:start] + examples[start + foldSize:len(examples)]
			error = self.matrix2Error(self.predMatrix(training, test), len(test))
			errSum += error
		return errSum / k


	def predMatrix(trainingData, testData):
		predMatrix = make2dList(10,10,0)
		
		for point in testExamples:
			(example, label) = point
			(ans, metaData) = self.knn.classify(trainingData, example)
			predMatrix[label][ans] += 1
		return predMatrix


	def matrix2Error(self, matrix, total):
		correct = 0
		for i in range(len(matrix)):
			correct += matrix[i][i]
		return correct / total
