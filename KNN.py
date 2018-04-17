
class KNN(object)
	
	def __init__(self,k):
		self.data = trainingData
		self.trainingInstances
		self.trainingLabels
		self.k = k

	def classify(self, example):
		nearestD = [self.k]
		nearestI = [self.k]

		for i in range(len(self.data)):
			point = self.trainingData[i]
			d = distance(example, point)
			if (ind = closer(nearest,d)) != -1:
				nearest[ind] = d
				nearestIndexes[ind] = i
				
		voters = [self.trainingLabels[i] for i in nearestIndexes]
		ans = vote(voters)
		return ans

	# if d is smaller than a value in nearest, return index to replace
	# else return -1
	def closer(nearest, d):
		for i in range(len(nearest)):
			distance = nearest[i]
			if(d < distance): return i
		return -1






	def distance(p1, p2):
		if(len(p1) != len(p2)):
			 raise ValueError("mismatched vector size")
	 	else:
	 		d = 0
	 		for i in range(len(p1)):
	 			d += (p[i] - p2[i]) ** 2
	 		return d
