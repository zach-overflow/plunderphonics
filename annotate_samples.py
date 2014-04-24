#! /usr/bin/env python

import os, sys
import wave, pyaudio

def play_wav(filename):
    """
    Source:
    http://stackoverflow.com/questions/17657103/how-to-play-wav-file-in-python
    """
    #define stream chunk   
    chunk = 1024  
    #open a wav format music  
    f = wave.open(filename, "rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  
    #play stream  
    while data != '':  
        stream.write(data)  
        data = f.readframes(chunk)  
    #stop stream  
    stream.stop_stream()  
    stream.close()  
    #close PyAudio  
    p.terminate()

if len(sys.argv) < 2:
    print "Usage: {0} <input_directory>".format(sys.argv[0])
    sys.exit(1)

input_dir = sys.argv[1]

# Recursively get all files from INPUT_DIR and store into FILES
files = []
for dir_name, subdir_list, file_list in os.walk(input_dir):
    for f in file_list:
        if dir_name[-1] != '/':
            dir_name = dir_name + '/'
        files.append('{0}{1}'.format(dir_name, f))

# Filter out all files which are not .WAV format
files = filter(lambda filename : '.wav' in filename, files)

print "Found {0} .wav files in directory {1}".format(len(files), input_dir)

# Get class configuration from user
classes = []
num_classes = int(raw_input("--> Enter number of classes : "))
for i in range(num_classes):
    class_name = raw_input("----> Enter label for class {0} : ".format(i))
    classes.append(class_name)
print "{0} classes saved : {1}".format(len(classes), classes)

# Configure output directory
output_dir_prompt = "Enter output directory : " 
output_dir = raw_input("--> " + output_dir_prompt)
while os.path.exists(output_dir):
    output_dir = raw_input("--> Error, directory/file already exists. " +
                            output_dir_prompt)

# Allowing user to label samples
i = 0
while i < len(files):
    cmd_prompt = "Current file: {0}\nEnter command (p: play, 0-9: class, s: skip, c: show classes) : ".format(files[i])
    cmd = raw_input("--> " + cmd_prompt).lower()
    while not cmd.isdigit() and cmd not in ["p", "s", "c"]:
        cmd = raw_input("--> Error, invalid command. " + cmd_prompt).lower()
    if cmd == "p":
        try:
            play_wav(files[i])
        except:
            print "Error trying to play file"
    elif cmd == "c":
        for j, c in enumerate(classes):
            print "{0} : {1}".format(j, c)
    elif cmd == "s":
        i = i + 1
    elif cmd.isdigit():
        pass
