import sys, os, wave, wavio, random, shutil
import aubio as a
import closest_drum
from numpy import array, vstack, zeros, append, delete, asarray

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
samples_for_mfcc = 3100
n_filters = 40
n_coeffs = 19


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
    output_dir = 'separated_input'
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
            shutil.move(output_filename, '{0}'.format(output_dir))
            samples_to_onset = onset_array[i] - start
            samples_to_onset_array.append([output_filename, samples_to_onset])
    with open(output_csv_filename, 'w') as csvfile:
        a = csv.writer(csvfile)
        a.writerows(samples_to_onset_array)
    shutil.move(output_csv_filename, '{0}'.format(output_dir))

extract_drums(attack, samples_for_mfcc, onsets, filename)

# compute MFCC for input file
separated_files = os.listdir('separated_input')
wav_files = filter(lambda f : '.wav' in f, separated_files)
csv_file = filter(lambda f : '.csv' in f, separated_files)[0]
samples_to_onset_dict = {}
with open('separated_input/{0}'.format(csv_file), 'r') as c:
    read = csv.reader(c)
    for row in reader:
        samples_to_onset_dict[os.path.basename(row[0])] = row[1]

hop_s = win_s / 4
temp_files = []
for wav in wav_files:
    wav_file_path = "separated_input/{0}".format(wav)
    samples_to_onset = int(samples_to_onset_dict[wav])
    readwav = wavio.readwav(wav_file_path)
    readwav_array = readwav[2]
    mfccwav_array = readwav_array[samples_to_onset : samples_to_onset + samples_for_mfcc]
    temp_filename = 'separated_input/{0}_temp.wav'.format(os.path.splitext(wav)[0])
    wavio.writewav24(temp_filename, readwav[0],mfccwav_array)
    temp_files.append(temp_filename)

csv_output = []

for temp_file in temp_files:
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
    mfccs = map(lambda v : delete(v, 0), mfccs)
    mfcc_col = array([])
    for m in mfccs:
        mfcc_col = append(mfcc_col, m)
    os.remove(temp_file)
    og_name = os.path.basename(temp_file)
    csv_output.append([og_name] + mfcc_col.aslist())

with open('input_mfcc.csv', 'w') as csvfile:
    write = csv.writer(csvfile)
    write.writerows(csv_output)

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
