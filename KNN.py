import numpy as np
import math


class KNN(object):
	
	def __init__(self,k):
		self.k = k

	def vote(self, voters):
		best = None
		mostVotes = 0
		votes = {}
		for vote in voters:
			if vote in votes:
				votes[vote] += 1
				if(votes[vote] > mostVotes):
					best = vote
					mostVotes = votes[vote]
			else:
				votes[vote] = 1
				if(votes[vote] > mostVotes):
					best = vote
					mostVotes = votes[vote]
		return best


	# if d is smaller than a value in nearest, return index to replace
	# else return -1
	def closer(self, nearest, d):
		for i in range(len(nearest)):
			distance = nearest[i]
			if(distance == -1 or d < distance): return i
		return -1


	def distance(self, p1, p2):
		d = 0
		diff = np.subtract(p1,p2)
		square = np.square(diff)
		sum0 = np.sum(square)
		return math.sqrt(sum0)
		

	def classify(self, trainingData, example):
		nearest = [-1] * self.k
		nearestIndexes = [-1] * self.k
		for i in range(len(trainingData)):
			point = trainingData[i][0]
			d = self.distance(example, point)
			ind = self.closer(nearest,d)
			if ind != -1:
				nearest[ind] = d
				nearestIndexes[ind] = i
				
		voters = [trainingData[i][1] for i in nearestIndexes]
		ans = self.vote(voters)
		metaData = list()
	
		for i in range(len(nearestIndexes)):
			exampleN = trainingData[nearestIndexes[i]][0]
			labelN =trainingData[nearestIndexes[i]][1]
			distanceN = nearest[i]
			metaData.append( (exampleN, labelN, distanceN))
		return ans, metaData
