#! /usr/bin/env python

import sys, wavio, csv, os
from aubio import source, pvoc, mfcc
from numpy import array, vstack, zeros, append, delete, asarray

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
# NOT USING THIS RIGHT NOW
ms_for_mfcc = 50

#samples_for_mfcc = int(samplerate * ms_for_mfcc * 0.001)

# temporary
samples_for_mfcc = 3100

if len(sys.argv) < 2:
    print "Usage: %s <source_directory>" % sys.argv[0]
    sys.exit(1)

source_directory = sys.argv[1]

files_in_src_dir = os.listdir(source_directory)
wav_files = filter(lambda f : '.wav' in f, files_in_src_dir)
csv_files = filter(lambda f : '.csv' in f, files_in_src_dir)

samples_to_onset_dict = {}

for csvfile in csv_files:
    with open('{0}/{1}'.format(source_directory, csvfile), 'r') as c:
        reader = csv.reader(c)
        for row in reader:
            samples_to_onset_dict[os.path.basename(row[0])] = row[1]

print samples_to_onset_dict

temp_files = []
for wav in wav_files:
    wav_file_path = "{0}{1}".format(source_directory, wav)
    samples_to_onset = int(samples_to_onset_dict[wav])
    readwav = wavio.readwav(wav_file_path)
    readwav_array = readwav[2] # sample data from the wav file of interest
    mfccwav_array = readwav_array[samples_to_onset: samples_to_onset + samples_for_mfcc]
    temp_filename = '{0}{1}_temp.wav'.format(source_directory, os.path.splitext(wav)[0])
    wavio.writewav24(temp_filename, readwav[0], mfccwav_array) # temp wav file that the mfcc's are calculated from
    temp_files.append(temp_filename)

csv_output = []

for temp_file in temp_files:
    # run mfcc analysis on the temp file
    samplerate = 0
    s = source(temp_file, samplerate, hop_s)
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
    # take the DCT term out
    mfccs = map(lambda v : delete(v, 0), mfccs)
    # collapse into column vector
    mfcc_column_vector = array([])
    for m in mfccs:
        mfcc_column_vector = append(mfcc_column_vector, m)
    # delete the temp file 
    os.remove('{0}'.format(temp_file))
    # associate the mfcc data with the wav file in some vector csv way.
    og_name = os.path.basename(temp_file)
    csv_output.append([og_name, asarray(mfcc_column_vector)])

with open('mfcc_data.csv', 'w') as csvfile:
    write = csv.writer(csvfile)
    write.writerows(csv_output)
