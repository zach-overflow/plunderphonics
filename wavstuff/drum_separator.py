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

def extract_drums(attack = 1500, onset_array = onsets, wavefile = sys.argv[1]):
    """
    extracts the individual drum hits from a wav file and writes them as separate wav files.
    attack and decay are in samples instead of milliseconds. So 44 samples is about 1 millisecond 
    for a second recorded at 44.1Khz samplerate.    
    The conditionals here need to be refined since the length of the subsequent wav files appear to be 
    slightly random.
    """
    read_data = wavio.readwav(wavefile)
    filename = os.path.splitext(wavefile)[0]
    read_array = read_data[2] # a list of sample values in sequential order for the wavefile
    for i in range(len(onset_array) - 1):
	    if onset_array[i + 1] >= len(read_array) and onset_array[i] - attack < 0:
	    	write_array = read_array[0:]
	    	wavio.writewav24('{0}_{1}.wav'.format(filename, "%05d" % i), read_data[0], write_array)
	    elif onset_array[i] - attack < 0:
	    	write_array = read_array[0: onset_array[i + 1]]
	    	wavio.writewav24('{0}_{1}.wav'.format(filename, "%05d" % i), read_data[0], write_array)
	    elif onset_array[i + 1] >= len(read_array):
	    	write_array = read_array[onset_array[i] - attack:]
	    	wavio.writewav24('{0}_{1}.wav'.format(filename, "%05d" % i), read_data[0], write_array)
	    else:
	    	write_array = read_array[onset_array[i] - attack: onset_array[i+1]]
	    	if i == 20: # for testing only
	    		print len(write_array)
	    	wavio.writewav24('{0}_{1}.wav'.format(filename, "%05d" % i), read_data[0], write_array)

extract_drums()
