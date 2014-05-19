# A script for extracting pitch information from chords - still in development
# See https://github.com/bmcfee/librosa/ for documentation on Librosa

import PyChoReLib.ChordRecognizer as cr
from PyChoReLib.Chord import Chord
import os, sys, scipy
import numpy as np
# import matplotlib as mpl
# mpl.use('Agg')
import librosa as l
#f rom matplotlib import pyplot

# specify path to audio files, directory to contain numpy arrays
audio_path = sys.argv[1]
out_path = sys.argv[2]

for audiofile in os.listdir(audio_path):

	if audiofile.endswith(".wav"):

		# Set 'y' to audio time series, 'sr' to sample rate
		y, sr = l.load(audio_path + audiofile)

		# Initialize the chromagram
		C = l.feature.chromagram(y=y, sr=sr, n_fft=4096, hop_length=64)

		# Uncomment to save chromagram to file
		np.save(out_path + "/" + audiofile[:-4], C)

		# The following can be uncommented to save a visual figure of the chromagram

		# # Make a new figure
		# pyplot.figure(figsize=(12,4))

		# # Display the chromagram: the energy in each chromatic pitch class as a function of time
		# # To make sure that the colors span the full range of chroma values, set vmin and vmax
		# l.display.specshow(C, sr=sr, hop_length=64, x_axis='time', y_axis='chroma', vmin=0, vmax=1)

		# pyplot.title('Chromagram for '+audio_path)
		# pyplot.colorbar()

		# pyplot.tight_layout()

		# # Save a .png of the chromagram.
		# pyplot.savefig(audio_path[:-4]+'.png')


