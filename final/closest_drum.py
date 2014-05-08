import sys, os, csv, wavio, copy
import aubio as a
import numpy as np

"""
This is where the magic happens. The drum vectors are associated with their nearest neighbor here.
The NN class describes the high-dimensional space where drum vectors reside. 
The drumVect class is associated with a drumhit's wavefile and mfcc vector as well as its classification.
"""

class NN:
	def __init__(self, trainedData, vectArray = []):
		"""
		trainedData is a dictionary of drumVects to their classification.
		"""
		self.trainedData = trainedData
		self.vectArray = vectArray

	def get_trainedData(self):
		"""
		returns the trainedData associated with the NN.
		"""
		return trainedData

	def get_vectArray(self):
		"""
		returns the vectArray associated with the NN.
		"""
		return self.vectArray

	def euclid_dist(self, drumVect1, drumVect2):
		"""
		calculates the euclidean distance between 2 drum vectors.
		"""
		if drumVect1.get_dimensions() != drumVect2.get_dimensions():
			raise ValueError("drum vectors are of different dimenions")
		else:
			d1 = drumVect1.get_numArray()
			d2 = drumVect2.get_numArray()
			eucDist = np.linalg.norm(d1-d2)
			return eucDist

	def k_closest(self, k, drumVect):
		"""
		finds the k closest vectors to the provided drum vector (drumVect).
		Returns these kVectors as a list where the closest vector is the first element.
		kList should be sorted such that the first element is the closest drumVect and the kth
		element is the farthest of the k drumVects from the provided drumVect.
		"""
		kList = [] # list of tuple. first elem is distance to provided drumVect, second elem is a drumVect object.
		minDist = float('inf')
		modVectArray = copy.copy(self.vectArray)
		modVectArray.remove(drumVect)
		for vector in modVectArray:
			dist = self.euclid_dist(drumVect, vector)
			if dist < minDist:
				minDist = dist
				if len(kList) == k:
					kList.remove(k - 1)
				kList.insert(0, (minDist, vector)) # place vector at front of kList
			else:
				if len(kList) == k:
					nearBool = False
					i = 0
					while i < len(kList):
						if kList[i][0] > dist:
							nearBool = True
							replaceIndex = i
							break
						i += 1
					if nearBool:
						kList.insert(replaceIndex, (dist, vector))
						kList.remove(k) 
				if len(kList) < k:
					i = 0
					while i < len(kList):
						if kList[i][0] > dist:
							replaceIndex = i
							kList.insert(replaceIndex, (dist, vector))
							break
						i += 1
		finalKList = []
		for closeK in kList:
			finalKList.append(closeK[1])
		return finalKList

	def add_vect(self, drumVect):
		"""
		adds a drumVect into the space.
		"""
		self.vectArray.append(drumVect)

	def remove_vect(self, drumVect):
		"""
		removes a drumVect from the space.
		"""
		self.vectArray.remove(drumVect)

class drumVect:
	def __init__(self, filename, numArray):
		self.filename = filename # used to identify specific vectors as well as finding the wavefile
		self.numArray = numArray # a numpy array representing the vector entries
		#self.classification = classification # a string (i.e. 'snare', 'kick', etc)

	#def get_wavefile(self):
		"""
		returns the wavefile of the drumhit associated with the drumVect of interest.
		file should be in {blank} directory
		"""
		# some csv bullshit

	def get_numArray(self):
		"""
		returns the numArray of the drumVect.
		"""
		return self.numArray

	def get_dimensions(self):
		"""
		returns the dimensions of the vector.
		"""
		dimensions = np.shape(self.numArray)
		return dimensions


	# def get_classification(self): 
	# 	"""
	# 	returns the classification of the drumVect.
	# 	"""
	# 	return self.classification


