#! /usr/bin/env python

import sys
from aubio import source, pvoc, mfcc
from numpy import array, vstack, zeros

win_s = 512                 # fft size
hop_s = win_s / 4           # hop size
n_filters = 40
n_coeffs = 13
samplerate = 44100

if len(sys.argv) < 2:
    print "Usage: %s <source_filename>" % sys.argv[0]
    sys.exit(1)

source_filename = sys.argv[1]

samplerate = 0
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

s = source(source_filename, samplerate, hop_s)
samplerate = s.samplerate
p = pvoc(win_s, hop_s)
m = mfcc(win_s, n_filters, n_coeffs, samplerate)

mfccs = zeros([13,])
frames_read = 0
while True:
    samples, read = s()
    spec = p(samples)
    mfcc_out = m(spec)
    mfccs = vstack((mfccs, mfcc_out))
    frames_read += read
    if read < hop_s: break

print "\nMOTHERFUCKING ARRAY : ", mfccs
print "\nMOTHERFUCKING DIMENSIONS : ", len(mfccs), " x ", len(mfccs[0])
