# a file for generating midi files of chords for chroma training
#
#
# currently generating all 12 major and minor triads at all 3 inversions

from midiutil.MidiFile import MIDIFile
import os, sys, getopt, glob, random, re, subprocess

NOTES = ['a','a#','b','c','c#','d','d#','e','f','f#','g','g#']

# loop for major/minor
for h in range(0,2):
	if h == 0:
		tonality = "major"
	else:
		tonality = "minor"

	# loop for notes, lowest note is A below middle C, midinote = 57
	for i in range(0,12):
		midiNotes = [0+i, (4+i-h)%12, (7+i)%12]
		midiNotes = map(lambda x: x+57, midiNotes)

		# loop for inversions
		for j in range(0,3):
			if j == 1:
				midiNotes[0] = midiNotes[0]+12
			if j == 2:
				midiNotes[1] = midiNotes[1]+12

			# Create the MIDIFile Object with 1 track
			MyMIDI = MIDIFile(1)

			# Tracks are numbered from zero. Times are measured in beats.
			track = 0   
			time = 0

			# Add track name and tempo.
			MyMIDI.addTrackName(track,time, NOTES[i]+"_"+tonality+"_"+str(j))
			MyMIDI.addTempo(track,time,120)

			# Add a note. addNote expects the following information:
			for midiNote in midiNotes:
				track = 0
				channel = 0
				pitch = midiNote
				time = 0
				duration = 4
				volume = 100

				# Now add the note.
				MyMIDI.addNote(track,channel,pitch,time,duration,volume)

			# And write it to disk.
			if not os.path.exists("midi_files"):
			    os.makedirs("midi_files")
			binfile = open(os.path.join("midi_files", NOTES[i]+"_"+tonality+"_"+str(j)+".mid"), 'wb')
			MyMIDI.writeFile(binfile)
			binfile.close()

# The following is borrowed code from 
# https://gist.githubusercontent.com/devonbryant/1810984/raw/b3056efda1eb2b14c9c92adaa26dd98c40459f0f/miditoaudio.py

"""
Copyright (C) 2012 Devon Bryant
"""
    
def is_fsynth_installed():
    """ Check to make sure fluidsynth exists in the PATH """
    for path in os.environ['PATH'].split(os.pathsep):
        f = os.path.join(path, 'fluidsynth')
        if os.path.exists(f) and os.access(f, os.X_OK):
            return True
        
    return False

def to_audio(sf2, midi_file, out_dir, out_type='wav', txt_file=None, append=True):
    """ 
    Convert a single midi file to an audio file.  If a text file is specified,
    the first line of text in the file will be used in the name of the output
    audio file.  For example, with a MIDI file named '01.mid' and a text file
    with 'A    major', the output audio file would be 'A_major_01.wav'.  If
    append is false, the output name will just use the text (e.g. 'A_major.wav')
    
    Args:
        sf2 (str):        the file path for a .sf2 soundfont file
        midi_file (str):  the file path for the .mid midi file to convert
        out_dir (str):    the directory path for where to write the audio out
        out_type (str):   the output audio type (see 'fluidsynth -T help' for options)
        txt_file (str):   optional text file with additional information of how to name 
                          the output file
        append (bool):    whether or not to append the optional text to the original
                          .mid file name or replace it
    """
    fbase = os.path.splitext(os.path.basename(midi_file))[0]
    if not txt_file:
        out_file = out_dir + '/' + fbase + '.' + out_type
    else:
        line = 'out'
        with open(txt_file, 'r') as f:
            line = re.sub(r'\s', '_', f.readline().strip())
            
        if append:
            out_file = out_dir + '/' + line + '_' + fbase + '.' + out_type
        else:
            out_file = out_dir + '/' + line + '.' + out_type

    subprocess.call(['fluidsynth', '-T', out_type, '-F', out_file, '-ni', sf2, midi_file])

def main():
    """
    Convert a directory of MIDI files to audio files using the following command line options:
    
    --sf2-dir (required)   the path to a directory with .sf2 soundfont files.  The script will 
                           pick a random soundfont from this directory for each file.
                           
    --midi-dir (required)  the path to a directory with the .mid MIDI files to convert.
    
    --out-dir (optional)   the directory to write the audio files to
    
    --type (optional)      the audio type to write out (see 'fluidsynth -T help' for options)
                           the default is 'wav'
                           
    --replace (optional)   if .txt files exist in the same directory as the .mid files, the text
                           from the files will be used for the output audio file names instead
                           of the midi file names.  If not specified, the text from the files will
                           be appended to the file name.
    """
    try:
        if not is_fsynth_installed():
            raise Exception('Unable to find \'fluidsynth\' in the path')
        
        opts, args = getopt.getopt(sys.argv[1:], None, ['sf2-dir=', 'midi-dir=', 'out-dir=', 'type=', 'replace'])
        sf2files, midifiles, textfiles, out_dir, out_type, append = [], [], [], None, 'wav', True
        for o, v in opts:
            if o == '--sf2-dir':
                sf2files = glob.glob(v + '/*.[sS][fF]2')
            elif o == '--midi-dir':
                midifiles = glob.glob(v + '/*.[mM][iI][dD]')
                textfiles = glob.glob(v + '/*.[tT][xX][tT]')
                if not out_dir:
                    out_dir = v
            elif o == '--out-dir':
                out_dir = v
            elif o == '--type':
                out_type = v
            elif o == '--replace':
                append = False
                
        if not sf2files:
            raise Exception('A --sf2-dir directory must be specified where at least one .sf2 file exists')
        elif not midifiles:
            raise Exception('A --midi-dir directory must be specified where at least one .mid file exists')

        if not textfiles or len(textfiles) < len(midifiles):
            for mid in midifiles:
                to_audio(random.choice(sf2files), mid, out_dir, out_type)
        else:
            for mid, txt in zip(midifiles, textfiles):
                to_audio(random.choice(sf2files), mid, out_dir, out_type, txt, append)
                    
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    except Exception, exc:
        print str(exc)
        sys.exit(2)
        
if __name__ == '__main__':
    sys.exit(main())
