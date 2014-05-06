#! /usr/bin/env python

import sys
from aubio import source, pvoc, mfcc
from numpy import array, vstack, zeros

# fft size
win_s = 512
# hop size
hop_s = win_s / 4
n_filters = 40
# number of MFCC coefficients. needs to be 1 more than actual number since
# we are discarding the first coefficient
n_coeffs = 19
samplerate = 44100
# milliseconds of data to compute MFCC for. 
# we need this to ensure that our MFCC matrix has the same dimensions
# for each drum hit file. 
ms_for_mfcc = 50

#samples_for_mfcc = int(samplerate * ms_for_mfcc * 0.001)

# temporary
samples_for_mfcc = 3100

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

mfccs = zeros([n_coeffs,])
frames_read = 0
while True:
    samples, read = s()
    spec = p(samples)
    mfcc_out = m(spec)
    mfccs = vstack((mfccs, mfcc_out))
    frames_read += read
    if read < hop_s: break
