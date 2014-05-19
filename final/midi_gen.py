# a file for generating midi files of chords for chroma training
#
#
# currently generating all 12 major and minor triads at all 3 inversions

from midiutil.MidiFile import MIDIFile
import os, sys, getopt, glob, random, re, subprocess

NOTES = ['a','a#','b','c','c#','d','d#','e','f','f#','g','g#']

# the 'A' from which chords are built
LOW_A = 57

for g in range(-3, 4):
	LOW_NOTE = LOW_A + (g*12)

	# loop for major/minor
	for h in range(0,2):
		if h == 0:
			tonality = "major"
		else:
			tonality = "minor"

		# loop for notes, lowest note is MIDDLE_A
		for i in range(0,12):
			midiNotes = [0+i, (4+i-h)%12, (7+i)%12]
			midiNotes = map(lambda x: x+LOW_NOTE, midiNotes)

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
				MyMIDI.addTrackName(track,time, NOTES[i]+"_"+tonality+"_"+str(g+3)+"_"+str(j))
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
				binfile = open(os.path.join("midi_files", NOTES[i]+"_"+tonality+"_"+str(g+3)+"_"+str(j)+".mid"), 'wb')
				MyMIDI.writeFile(binfile)
				binfile.close()