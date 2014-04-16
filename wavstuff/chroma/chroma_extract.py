# A script for extracting pitch information from chords - still in development
# See https://github.com/bmcfee/librosa/ for documentation on Librosa

import PyChoReLib.ChordRecognizer as cr
from PyChoReLib.Chord import Chord
import os, sys, scipy
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import librosa as l
from matplotlib import pyplot

audio_path = sys.argv[1]

# Set 'y' to audio time series, 'sr' to sample rate
y, sr = l.load(audio_path)

# Initialize the chromagram
C = l.feature.chromagram(y=y, sr=sr, n_fft=4096, hop_length=64)

# Calculate mean intensity for chromagram and each note
mean = np.mean(C)
Cmean = np.apply_along_axis(np.mean, axis=1, arr=C)

print Cmean

NOTES = ['a','a#','b','c','c#','d','d#','e','f','f#','g','g#']

nArray = []
for i in range(0, 12):
	if Cmean[i] > 0.5:
		nArray.append(NOTES[i])

# Initialize chord recognizer, ideally this would be done externally as initializing
# the knowledge base is a timely procedure.
R = cr.ChordRecognizer()
R.InitializeKnowledgeBase()

# chord = R.RecognizeChord(Chord(nArray))
# print chord

# Uncomment to save chromagram to file
np.savetxt(audio_path[:-4]+'.txt', C, fmt='%10.5f')

# The following can be uncommented to save a visual figure of the chromagram

# Make a new figure
pyplot.figure(figsize=(12,4))

# Display the chromagram: the energy in each chromatic pitch class as a function of time
# To make sure that the colors span the full range of chroma values, set vmin and vmax
l.display.specshow(C, sr=sr, hop_length=64, x_axis='time', y_axis='chroma', vmin=0, vmax=1)

pyplot.title('Chromagram for '+audio_path)
pyplot.colorbar()

pyplot.tight_layout()

# Save a .png of the chromagram.
pyplot.savefig(audio_path[:-4]+'.png')


