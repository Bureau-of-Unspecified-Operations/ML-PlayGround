
class KNN(object):
	
	def __init__(self,k,data, labels):
		self.data = data
		self.label = labels
		self.k = k

	def classify(self, example):
		nearest = [self.k]
		nearestIndexes = [self.k]

		for i in range(len(self.data)):
			point = self.data[i]
			d = distance(example, point)
			ind = closer(nearest,d)
			if ind != -1:
				nearest[ind] = d
				nearestIndexes[ind] = i
				
		voters = [self.labels[i] for i in nearestIndexes]
		ans = vote(voters)
		return ans

	def train(self, data, label):
		self.data.append(data)
		self.label.append(label)

	def vote(voters):
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
	def closer(nearest, d):
		for i in range(len(nearest)):
			distance = nearest[i]
			if(d < distance): return i
		return -1






	def distance(p1, p2):
 		d = 0
 		for i in range(len(p1)):
 			d += (p[i] - p2[i]) ** 2
 		return d
