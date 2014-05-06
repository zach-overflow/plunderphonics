import os, sys, wavio, random, shutil
import aubio as a
import csv

"""
The start and end values for these functions are in samples, not in seconds.
At the moment only 24 bit wav files can be used. If using AIFF files or other
formats, you will have to convert to 24 bit wav first.
"""

win_s = 512         #fft size
hop_s = win_s / 2   #hop size
samplerate = 0

def extract_drums(attack, decay, onset_array, wavefile):
	"""
	extracts the individual drum hits from a wav file and writes them as separate wav files.
	attack and decay are in samples instead of milliseconds. So 44 samples is about 1 millisecond 
	for a second recorded at 44.1Khz samplerate.    
	The conditionals here need to be refined since the length of the subsequent wav files appear to be 
	slightly random. It was found that an attack time of 1500 samples works well for drum transients.
	If the transient is too short (2200 samples =~50 ms not including the attack time), the file for 
	that drum hit is not written as it will not be useful.
	"""
	read_data = wavio.readwav(wavefile)
	filename = os.path.splitext(wavefile)[0]
	read_array = read_data[2] # a list of sample values in sequential order for the wavefile
	output_csv_filename = '{0}_samples_to_onset.csv'.format(filename)
	samples_to_onset_array = []
	for i in range(len(onset_array) - 1):
		if onset_array[i + 1] >= len(read_array) and onset_array[i] - attack < 0:
			start = 0
			write_array = read_array[0:]
		elif onset_array[i] - attack < 0:
			start = 0
			write_array = read_array[0: onset_array[i + 1]]
		elif onset_array[i + 1] >= len(read_array):
			start = onset_array[i] - attack
			write_array = read_array[onset_array[i] - attack:]
		else:
			start = onset_array[i] - attack
			write_array = read_array[onset_array[i] - attack: onset_array[i+1]]
		if len(write_array) - attack >= decay: #if the drumhit file is long enough, write it into the unclassified_drums directory
			output_filename = '{0}_{1}.wav'.format(filename, "%05d" % i)
			wavio.writewav24(output_filename, read_data[0], write_array)
			shutil.move(output_filename, 'unclassified_drums')
			samples_to_onset = onset_array[i] - start
			samples_to_onset_array.append([output_filename, samples_to_onset])
	with open(output_csv_filename, 'w') as csvfile:
		a = csv.writer(csvfile)
		a.writerows(samples_to_onset_array)
	shutil.move(output_csv_filename, 'unclassified_drums')

fileList = os.listdir('./unseparated_drums') #list of drum files in unseparated_drums directory
fileList = filter(lambda f : '.wav' in f, fileList)

while len(fileList) > 0: #iterate through all unseparated drum clips in unseparated_drums directory
	filename = './unseparated_drums/{0}'.format(fileList[0])
	s = a.source(filename, samplerate, hop_s)
	samplerate = s.samplerate
	o = a.onset("default", win_s, hop_s, samplerate)
	onsets = [] # a list of onsets in samples
	total_frames = 0 # total number of frames read
	while True:
		samples, read = s()
		if o(samples):
			#print "%f" % o.get_last_s() # for testing purposes
			onsets.append(o.get_last())
		total_frames += read
		if read < hop_s: break
	extract_drums(1500, 3100, onsets, filename)
	del fileList[0] #remove clip from list of drum files to separate
print 'DONE, BRO!'


