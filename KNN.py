import numpy as np
import math


class KNNModel(object):
	
	def __init__(self,k):
		self.k = k
		self.data = None
		self.lastClassified = None
		self.lastHelpExamples = list()
		self.lastHelpDistances = list()
		self.lastHelpLabels = list()

	def incK(self):
		self.k += 1

	def decK(self):
		if k > 1:
			self.k -= 1

	def clearHelpers(self):
		del self.lastHelpExamples[:]
		del self.lastHelpDistances[:]
		del self.lastHelpLabels[:]

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

	def train(self, data):
		self.data = data

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
		

	def classify(self, example):
		self.lastClassified = example
		self.clearHelpers()
		nearest = [-1] * self.k
		nearestIndexes = [-1] * self.k
		for i in range(len(self.data)):
			point = self.data[i][0]
			d = self.distance(example, point)
			ind = self.closer(nearest,d)
			if ind != -1:
				nearest[ind] = d
				nearestIndexes[ind] = i
				
		voters = [self.data[i][1] for i in nearestIndexes]
		ans = self.vote(voters)
		metaData = list()
	
		for i in range(len(nearestIndexes)):
			exampleN = self.data[nearestIndexes[i]][0]
			labelN = self.data[nearestIndexes[i]][1]
			distanceN = nearest[i]
			self.lastHelpExamples.append(exampleN)
			self.lastHelpLabels.append(labelN)
			self.lastHelpDistances.append(distanceN)
		return ans
