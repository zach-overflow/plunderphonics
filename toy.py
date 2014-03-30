'''
Chops up drum audio files into smaller audio files based on onset 
'''

import aubio as a
import sys
import os.path

def new_sink_name(filename_without_ext, slice_n, duration = duration):
    return filename_without_ext + '_%02.3f' % (slice_n*duration) + '.wav'

win_s = 512         # fft size
hop_s = win_s / 2   # hop size
samplerate = 0

filename = sys.argv[1]

filename_without_ext = os.path.splitext(os.path.basename(filename))[0]

s = a.source(filename, samplerate, hop_s)

samplerate = s.samplerate

o = a.onset("default", win_s, hop_s, samplerate)

onsets = []

# total number of frames read
total_frames = 0 
while True:
    samples, read = s() 
    if o(samples):
        onsets.append(o.get_last())
    total_frames += read
    if read < hop_s: break

# generate shit

g = a.sink(new_sink_name(filename_without_ext, 0), samplerate)


