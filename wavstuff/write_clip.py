import os, sys, wavio, random


def write_clip(start, end, clipname, wavefile = sys.argv[1]):
	"""The start and end values should be in samples, not seconds.
	   This can only be used on 24 bit wav files. If using AIFF or
	   any other type of file, conversion to 24 bit wav will be required first."""
	read_data = wavio.readwav(wavefile)
	read_array = read_data[2]
	write_array = []
	for i in range(start, end + 1):
		write_array.append(read_array[i])
	write_wav = wavio.writewav24('{0}.wav'.format(clipname), read_data[0], write_array)
