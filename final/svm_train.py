# build appropriate weight vectors for each major and minor triad using SVM
# output vectors stored as numpy arrays in directory weight_vectors
#
# argument 1: path to training data
# argument 2: path to testing data

import os, sys
import numpy as np
from sklearn import svm

CHORDS = ["a_major", "a#_major", "b_major", "c_major", "c#_major",
	"d_major", "d#_major", "e_major", "f_major", "f#_major",
	"g_major", "g#_major", "a_minor", "a#_minor", "b_minor",
	"c_minor", "c#_minor", "d_minor", "d#_minor", "e_minor", 
	"f_minor", "f#_minor", "g_minor", "g#_minor"]

# first argument is directory containing training data
train_path = sys.argv[1]
test_path = sys.argv[2]

# set frame-size for chroma analysis
FRAMESIZE = 100

# 'X' is a list of feature vectors for training
X = []

# 'y' is a corresponding list of classifiers
y = []

# process feature arrays in train_path, add them to 'X', classifiers to 'y'
for ftr_file in os.listdir(train_path):

	if ftr_file.endswith(".npy"):

		C = CHORDS.index(ftr_file[:-8])

		ftr_array = np.load(train_path+"/"+ftr_file)

		for i in range(0, (ftr_array.shape[1]//FRAMESIZE) - 1):
			feature_frame = ftr_array[:,i*FRAMESIZE:(i+1)*FRAMESIZE]
			X.append(feature_frame.mean(1))
			y.append(C)

# build and train the SVC
clf = svm.SVC(probability=True)
clf.fit(X, y)

# TEST MATCHING WINDOW TO WINDOW
		
# 'U' is a list of feature vectors for testing
U = []

# 'v' is a corresponding list of classifiers
v = []

# process feature arrays in test_path, add them to 'U', classifiers to 'v'
for ftr_file in os.listdir(test_path):

	if ftr_file.endswith(".npy"):

		C = CHORDS.index(ftr_file[:-8])

		ftr_array = np.load(test_path+"/"+ftr_file)

		for i in range(0, (ftr_array.shape[1]//FRAMESIZE) - 1):
			feature_frame = ftr_array[:,i*FRAMESIZE:(i+1)*FRAMESIZE]
			U.append(feature_frame.mean(1))
			v.append(C)

# evaluate score over 'U' and 'v'
score = clf.score(U, v)
print "Window-to-window score: ", score

# TEST MATCHING FILE TO WINDOW USING PROBABILISTIC WEIGHTING
		
# process feature arrays in test_path, weight windows by
# individual probability to determine chord of overall file

s_size = float(0)
s_correct = 0

for ftr_file in os.listdir(test_path):

	# 'U' is now a list of window feature vectors for evaluation
	U = []

	if ftr_file.endswith(".npy"):

		C = CHORDS.index(ftr_file[:-8])

		ftr_array = np.load(test_path+"/"+ftr_file)

		for i in range(0, (ftr_array.shape[1]//FRAMESIZE) - 1):
			feature_frame = ftr_array[:,i*FRAMESIZE:(i+1)*FRAMESIZE]
			U.append(feature_frame.mean(1))

		probs = clf.predict_log_proba(U).sum(0)
		class_index = probs.argmax()
		if class_index == C:
			s_correct += 1

		s_size += 1

new_score = float(s_correct /s_size)
print "Probability-weighted score: ", new_score

# BUILD A CLASSIFIER FOR MINOR/MAJOR, THEN TWO CLASSIFIERS FOR CHROMA

# 'X' is a list of feature vectors for training
X = []

# 'y' is a corresponding list of classifiers
y = []

# process feature arrays in train_path, add them to 'X', classifiers to 'y'
for ftr_file in os.listdir(train_path):

	if ftr_file.endswith(".npy"):

		if "major" in ftr_file:
			C = 0
		else:
			C = 1

		ftr_array = np.load(train_path+"/"+ftr_file)

		for i in range(0, (ftr_array.shape[1]//FRAMESIZE) - 1):
			feature_frame = ftr_array[:,i*FRAMESIZE:(i+1)*FRAMESIZE]
			X.append(feature_frame.mean(1))
			y.append(C)

#build and train the SVC
minmaj_clf = svm.SVC(probability=True)
minmaj_clf.fit(X, y)

##############################
# build major classifier now #
##############################

# 'X' is a list of feature vectors for training
X = []

# 'y' is a corresponding list of classifiers
y = []

# process feature arrays in train_path, add them to 'X', classifiers to 'y'
for ftr_file in os.listdir(train_path):

	if ftr_file.endswith(".npy") and "major" in ftr_file:

		C = CHORDS.index(ftr_file[:-8])

		ftr_array = np.load(train_path+"/"+ftr_file)

		for i in range(0, (ftr_array.shape[1]//FRAMESIZE) - 1):
			feature_frame = ftr_array[:,i*FRAMESIZE:(i+1)*FRAMESIZE]
			X.append(feature_frame.mean(1))
			y.append(C)

# build and train the SVC
maj_clf = svm.SVC(probability=True)
maj_clf.fit(X, y)

##############################
# build minor classifier now #
##############################

# 'X' is a list of feature vectors for training
X = []

# 'y' is a corresponding list of classifiers
y = []

# process feature arrays in train_path, add them to 'X', classifiers to 'y'
for ftr_file in os.listdir(train_path):

	if ftr_file.endswith(".npy") and "minor" in ftr_file:

		C = CHORDS.index(ftr_file[:-8]) - 12

		ftr_array = np.load(train_path+"/"+ftr_file)

		for i in range(0, (ftr_array.shape[1]//FRAMESIZE) - 1):
			feature_frame = ftr_array[:,i*FRAMESIZE:(i+1)*FRAMESIZE]
			X.append(feature_frame.mean(1))
			y.append(C)

# build and train the SVC
min_clf = svm.SVC(probability=True)
min_clf.fit(X, y)

# NOW RUN PROBABILITY WEIGHTED TESTS WITH MIN/MAJ METHOD

mm_size = float(0)
mm_correct = 0

s_size = float(0)
s_correct = 0

for ftr_file in os.listdir(test_path):

	# 'U' is now a list of window feature vectors for evaluation
	U = []

	if ftr_file.endswith(".npy"):

		C = CHORDS.index(ftr_file[:-8])

		ftr_array = np.load(test_path+"/"+ftr_file)

		for i in range(0, (ftr_array.shape[1]//FRAMESIZE) - 1):
			feature_frame = ftr_array[:,i*FRAMESIZE:(i+1)*FRAMESIZE]
			U.append(feature_frame.mean(1))

		minmaj_probs = minmaj_clf.predict_log_proba(U).sum(0)
		class_index = minmaj_probs.argmax()
		tonality = minmaj_probs.argmax()
		if (tonality == 0 and "major" in ftr_file) or (tonality == 1 and "minor" in ftr_file):
			mm_correct += 1

		mm_size += 1
		
		if tonality == 0:
			maj_probs = maj_clf.predict_log_proba(U).sum(0)
			class_index = maj_probs.argmax()
			if C == class_index:
				s_correct += 1
		else:
			min_probs = min_clf.predict_log_proba(U).sum(0)
			class_index = min_probs.argmax() + 12
			if C == class_index:
				s_correct += 1

		s_size += 1

mm_score = float(mm_correct/mm_size)
print "Bipartite mm score: ", mm_score

minmaj_score = float(s_correct /s_size)
print "Minor-major score: ", minmaj_score


