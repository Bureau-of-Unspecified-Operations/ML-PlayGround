
class KNN(object):
	
	def __init__(self,k,data, labels):
		self.data = data
		self.labels = labels
		self.k = k

	

	def train(self, data, label):
		self.data.append(data)
		self.labels.append(label)

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
		for i in range(len(p1)):
			d += (p1[i] - p2[i]) ** 2
		return d


	def classify(self, example):
		nearest = [-1] * self.k
		nearestIndexes = [-1] * self.k
		print(type(self.data[0]))
		print(type(self.labels[0]))
		for i in range(len(self.data)):
			point = self.data[i]
			d = self.distance(example, point)
			ind = self.closer(nearest,d)
			if ind != -1:
				nearest[ind] = d
				nearestIndexes[ind] = i
				
		voters = [self.labels[i] for i in nearestIndexes]
		ans = self.vote(voters)
		return ans
