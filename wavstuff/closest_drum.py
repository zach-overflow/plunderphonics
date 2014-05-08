import sys, os, numpy, csv, wavio
import aubio as a

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
		return vectArray

	def euclid_dist(self, drumVect1, drumVect2):
		"""
		calculates the euclidean distance between 2 drum vectors.
		"""
		if drumVect1.get_dimensions() != drumVect2.get_dimensions():
			raise ValueError("drum vectors are of different dimenions")
		else:
			eucDist = np.linalg.norm(drumVect1-drumVect2)
			return eucDist

	def k_closest(self, k, drumVect):
		"""
		finds the k closest vectors to the provided drum vector (drumVect).
		"""

	def add_vect(self, drumVect):
		"""
		adds a drumVect into the space.
		"""

	def remove_vect(self, drumVect):
		"""
		removes a drumVect from the space.
		"""

class drumVect:
	def __init__(self, filename, numArray, classification):
		self.filename = filename # used to identify specific vectors as well as finding the wavefile
		self.numArray = numArray # a numpy array representing the vector entries
		self.classification = classification # a string (i.e. 'snare', 'kick', etc)

	def get_wavefile(self):
		"""
		returns the wavefile of the drumhit associated with the drumVect of interest.
		file should be in {blank} directory
		"""

	def get_classification(self):
		"""
		returns the classification of the drumVect.
		"""
		return classification

	def get_numArray(self):
		"""
		returns the numArray of the drumVect.
		"""
		return numArray

	def get_dimensions(self):
		"""
		returns the dimensions of the vector.
		"""
		dimensions = np.shape(self.numArray)
		return dimensions

