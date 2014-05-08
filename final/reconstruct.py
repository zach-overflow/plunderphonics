import sys, os, wave, wavio, random, shutil
import aubio as a
import closest_drum

"""
This program takes a given drum clip and replaces each individual hit with a similar-sounding hit from
/separated_corpus by using the vectSpace and drumVect objects from closest_drum.
"""

if len(sys.argv) != 3:
	print ""
	sys.exit(1)

win_s = 512            # fft size
hop_s = win_s / 2      # hop size
samplerate = 0         # compiler bullshit
filename = sys.argv[1] # the drum clip we are replacing
attack = 1500          # attack value in samples, not seconds
corpus = sys.argv[2]   # the corpus of separated drum hits (a csv file)


#finds the onsets within the drum clip we are replacing
s = a.source(filename, samplerate, hop_s)
samplerate = s.samplerate
o = a.onset("default", win_s, hop_s, samplerate)
onsets = [] # a list of onsets in samples
total_frames = 0 # total number of frames read
while True:
	samples, read = s()
	if o(samples):
		onsets.append(o.get_last())
	total_frames += read
	if read < hop_s: break

# get samples to onset csv for the input file


def main():
	"""
	writes the new file which will show up in the current directory as {filename}replaced.wav
	at the moment the replacement method is a simple prototype without using any ML yet.
	Once we are able to find the most similar-sounding drumhit this will obviously have to change.
	"""
	similarDrums = os.listdir('./separated_corpus') # list of drumhit filenames directory.
	similarDrums = filter(lambda f : '.wav' in f, fileList)
	vSpace = closest_drum.vectSpace([],[]) # the vectSpace object to find the closest-souding drumhit.
	csvList = []
	# csvList is made of a list of tuples of form ({filename}, {mfcc numpy array})
	with open('mfcc_data.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			csvList.append([row[0], array(map(lambda e : float(e), row[1:]))])
	# create drumVect objects from each entry in csvList and add said drumVect to vSpace
	for elem in csvList:
		dVect = closest_drum.drumVect('{0}'.format(elem[0]), elem[1])
		vSpace.add_vect(dVect)
	# create a drumVect object from the input .wav
	inVect = closest_drum.drumVect('{0}'.format(filename), )
	"""
	make a drumVect object from the provided file (sys.argv[1])
	find the closest drum hit from the vectSpace to the above drumVect ojbect and assign to replacedHit
	"""

	w = wavio.readwav(sys.argv[1])
	writeArray = w[2] #a copy of the data from the original file supplied. modifying this.
	hit = 0
	while hit < len(onsets):
		if onsets[hit] - attack < 0:
			start = onsets[hit]
		else:
			start = onsets[hit] - 1500
		if hit == len(onsets) - 1:
			nextHit = None
		else: 
			nextHit = onsets[hit + 1] 
		replacedHit =  #our replacement hit.
		repl = wavio.readwav('./unclassified_drums/{0}'.format(replacedHit)) #file of replacement hit
		replacedHitArray = repl[2] #sample array
		if nextHit != None:
			#the replacedHitArray is longer than the distance between current and next hit
			if len(writeArray[start: nextHit + 1]) < len(replacedHitArray):
				writeArray[start: nextHit + 1] = replacedHitArray[0: len(writeArray[start: nextHit + 1])]
			#the replacedHitArray is shorter or equal to distance between current and next hit 
			else: 
				writeArray[start: start + len(replacedHitArray)] = replacedHitArray
		elif nextHit == None:
			#if the replacedHitArray is longer than the rest of the writeArray or both equal length
			if len(writeArray[start:]) <= len(replacedHitArray):
				writeArray[start:] = replacedHitArray[0: len(writeArray[start:])]
			#if the replacedHitArray is shorter than or equal to the rest of the writeArray
			else:
				writeArray[start: start + len(replacedHitArray)] = replacedHitArray
		hit += 1 
	wavio.writewav24('{0}replaced.wav'.format(filename[:len(filename) - 4]), w[0], writeArray) #save the replaced drum file as a new file.
	shutil.move('{0}replaced.wav'.format(filename[:len(filename) - 4]), './replaced_drums')

main()








