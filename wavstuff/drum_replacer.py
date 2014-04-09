import os, sys, wavio, random
import aubio as a

"""The start and end values for these functions are in samples, not in seconds.
   At the moment only 24 bit wav files can be used. If using AIFF files or other
   formats, you will have to convert to 24 bit wav first."""


"""adapted from the aubio onset demo. Returns a list of onsets
   (in samples) that appear in the wavefile."""
win_s = 512         #fft size
hop_s = win_s / 2   #hop size
samplerate = 0
filename = sys.argv[1]
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
# i = 0
# while i < len(onsets):
# 	print onsets[i]
# 	i += 1


def extract_drums(attack, decay, onset_array = onsets, wavefile = sys.argv[1]):
	"""extracts the individual drum hits from a wav file and writes them as separate wav files.
	   attack and decay are in samples instead of milliseconds. So 44 samples is about 1 millisecond 
	   for a second recorded at 44.1Khz samplerate."""
	read_data = wavio.readwav(wavefile)
	read_array = read_data[2] # a list of sample values in sequential order for the wavefile
	for i in range(len(onset_array)):
		if i - attack < 0 and i + decay:
			#do some shit
		elif i - attack < 0:
			#do some other shit
		elif i + decay > len(read_array):
			#do some other other shit
		else: 
			


def write_clip(start, end, clipname, wavefile = sys.argv[1]):
	read_data = wavio.readwav(wavefile) 
	read_array = read_data[2] # a list of sample values in sequential order for the wavefile
	write_array = []
	for i in range(start, end + 1):
		write_array.append(read_array[i])
	write_wav = wavio.writewav24('{0}.wav'.format(clipname), read_data[0], write_array)

def replace_drum(start, end, replacement_file, wavefile):
	"""replaces a singular drum hit in the wavefile with a replacement drum hit
	   from the replacement_file"""
	read_data = wavio.readwav(wavefile) 
	read_array = read_data[2] # a list of sample values in sequential order for the wavefile.
	replace_data = wavio.readwav(replacement_file)
	replace_array = replace_data[2] # a list of sample values in sequential order for the replacement file.
	i = 0
	while i < len(replace_array):
		read_array[i + start] = replace_array[i]
		i += 1



