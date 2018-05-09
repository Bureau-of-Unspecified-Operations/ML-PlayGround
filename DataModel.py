from pathlib import Path
import sys
import numpy as np
import pickle

class DataModel(object):
	filePath = "dataset.p"


	#data stored in pickle, when loaded it's a list of
	def __init__(self):
		dataFile = Path(self.filePath)
		if dataFile.is_file():
			print("loaded succesfully")
			self.dataset = pickle.load(open(self.filePath, "rb"))
		else:
			assert(1 == 2)
			self.dataset = [(datas[i], labels[i]) for i in range(len(datas))]

		self.workingset = self.dataset

	def clearWorkingset(self):
		self.workingset = list()

	def addAll2Workingset(self):
		self.workingset = self.dataset

	def getFrequencyTable(self):
		datadict = dict()
		for pair in self.workingset:
			label = pair[1]
			if label in datadict:
				datadict[label] += 1
			else: datadict[label] = 1
		return datadict

	def addEvenSubset2Working(self, percent):
		datadict = self.getFrequencyTable
		quotadict = dict()
		cntdict = dict()
		subset = list()
		#
		# Load quota dict and zero cnt
		for key in datadict.keys():
			quotadict[key] = datadict[key] * percent
			cntdict[key] = 0

		for pair in self.workingset:
			label = pair[1]
			if cntdict[label] < quotadict[label]:
				subset.append(pair)
				cntdict[label] += 1

		return subset

	def getWorkingset(self):
		return self.workingset


	def save(self):
		pickle.dump(self.dataset,open(self.filePath, "wb"))