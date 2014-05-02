import sys, os, wave, wavio, random, shutil
import aubio as a

"""
At the moment this program looks at a drum clip and simply replaces each drum hit with
another **random** drumhit within the unclassified_drums directory. Once we have a propper
classification system up and running, this program will be changed to replace a drum clip's
individual transients with similar-sounding transients.
"""

win_s = 512            #fft size
hop_s = win_s / 2      #hop size
samplerate = 0         #compiler bullshit
filename = sys.argv[1] #the drum clip we are replacing
attack = 1500          #attack value in samples, not seconds.

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

def main():
	"""
	writes the new file which will show up in the current directory as {filename}replaced.wav
	at the moment the replacement method is a simple prototype without using any ML yet.
	Once we are able to find the most similar-sounding drumhit this will obviously have to change.
	"""
	randDrums = os.listdir('./unclassified_drums') #list of drumhit filenames directory.
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
		replacedHit = random.choice(randDrums) #our replacement hit.
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








