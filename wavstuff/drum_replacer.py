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
# 	if i == 0:
# 		print 'fuckdapolice'
# 	print onsets[i]
# 	i += 1

#def extract_drums(attack = 200, decay = 4000, onset_array = onsets, wavefile = sys.argv[1]):
def extract_drums(onset_array = onsets, wavefile = sys.argv[1]):
	"""extracts the individual drum hits from a wav file and writes them as separate wav files.
	   attack and decay are in samples instead of milliseconds. So 44 samples is about 1 millisecond 
	   for a second recorded at 44.1Khz samplerate.

	   The conditionals here need to be refined since the length of the subsequent wav files appear to be 
	   slightly random. """
	read_data = wavio.readwav(wavefile)
	read_array = read_data[2] # a list of sample values in sequential order for the wavefile
	for i in range(len(onset_array) - 1):
		if onset_array[i + 1] >= len(read_array):
			write_array = read_array[onset_array[i]:]
			wavio.writewav24('drumhit{0}.wav'.format(i), read_data[0], write_array)
		else:
			write_array = read_array[onset_array[i]: onset_array[i+1]]
			wavio.writewav24('drumhit{0}.wav'.format(i), read_data[0], write_array)

		#the attack is longer than the start of the wavefile to the i'th onset 
		#AND the decay is longer than the dist from i'th onset and end of wavefile.

		# if onset_array[i] - attack < 0 and onset_array[i] + decay >= len(read_array): 
		# 	write_array = read_array[onset_array[i]: onset_array[i+1]]
		# 	wavio.writewav24('drumhit{0}.wav'.format(i), read_data[0], write_array)
		# #the attack is longer than the start of the wavefile to the i'th onset
		# elif onset_array[i] - attack < 0: 
		# 	write_array = read_array[onset_array[i]: onset_array[i] + decay]
		# 	wavio.writewav24('drumhit{0}.wav'.format(i), read_data[0], write_array)
		# #the decay is longer than the dist from the i'th onset and the end of the wavefile.
		# elif onset_array[i] + decay > len(read_array):
		# 	write_array = read_array[onset_array[i] - attack: onset_array[len(onset_array) - 1]]
		# 	wavio.writewav24('drumhit{0}.wav'.format(i), read_data[0], write_array)
		# #the attack plus the decay do not cause indexing errors so the total drumhit{i}.wav file
		# #is of length attack + decay samples.
		# else:
		# 	write_array = read_array[onset_array[i] - attack: onset_array[i] + decay] 
		# 	wavio.writewav24('drumhit{0}.wav'.format(i), read_data[0], write_array)

extract_drums()

# def write_clip(start, end, clipname, wavefile = sys.argv[1]):
# 	read_data = wavio.readwav(wavefile) 
# 	read_array = read_data[2] # a list of sample values in sequential order for the wavefile
# 	write_array = []
# 	for i in range(start, end + 1):
# 		write_array.append(read_array[i])
# 	write_wav = wavio.writewav24('{0}.wav'.format(clipname), read_data[0], write_array)

# def replace_drum(start, end, replacement_file, wavefile):
# 	"""replaces a singular drum hit in the wavefile with a replacement drum hit
# 	   from the replacement_file"""
# 	read_data = wavio.readwav(wavefile) 
# 	read_array = read_data[2] # a list of sample values in sequential order for the wavefile.
# 	replace_data = wavio.readwav(replacement_file)
# 	replace_array = replace_data[2] # a list of sample values in sequential order for the replacement file.
# 	i = 0
# 	while i < len(replace_array):
# 		read_array[i + start] = replace_array[i]
# 		i += 1



