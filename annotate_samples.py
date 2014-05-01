#! /usr/bin/env python

import os, sys
import wave, pyaudio
import csv

def play_wav(filename):
    """
    Plays a WAV file using PyAudio
    Taken from
    http://stackoverflow.com/questions/17657103/how-to-play-wav-file-in-python
    """
    # Define stream chunk
    chunk = 1024  
    # Open a wav format music  
    f = wave.open(filename, "rb")  
    # Instantiate PyAudio  
    p = pyaudio.PyAudio()
    # Open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    # Read data  
    data = f.readframes(chunk)  
    # Play stream  
    while data != '':  
        stream.write(data)  
        data = f.readframes(chunk)  
    # Stop stream  
    stream.stop_stream()  
    stream.close()  
    # Close PyAudio  
    p.terminate()


def main():
    """
    Given a directory as a command line argument, this script recursively
    collects all .WAV files from the directory (and its subdirectories),
    and allows the user to label each .WAV file with a certain class. The
    script also asks the user for the number of classes and their names. 
    It then saves the name of the original file, along with the labelled
    class to a CSV file.
    The format of this CSV file is -
    <filename with relative path>, <label index>, <label name>
    """
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

    # Get name for output CSV file
    output_file_prompt = "Enter name of output csv file : " 
    output_file = raw_input("--> " + output_file_prompt)
    while os.path.exists(output_file):
        output_file = raw_input("--> Error, directory/file already exists. " +
                                output_file_prompt)

    # Ask user to label samples one-by-one, store results in TO_WRITE
    to_write = []
    i = 0
    while i < len(files):
        cmd_prompt = "Current file: {0}\nEnter command (p: play, [number]: annotate class, s: skip, c: list classes) : ".format(files[i])
        cmd = raw_input("--> " + cmd_prompt).lower()
        # If the user is a dumbass
        while not cmd.isdigit() and cmd not in ["p", "s", "c"]:
            if cmd.isdigit():
                class_index = int(cmd)
                if class_index >= len(classes):
                    cmd = raw_input("--> Error, invalid class index. "
                                    + cmd_prompt).lower()
            else:
                cmd = raw_input("--> Error, invalid command. " 
                                + cmd_prompt).lower()
        if cmd == "p":
            try:
                play_wav(files[i])
            except:
                # PyAudio may be problematic
                print "Error trying to play file"
        elif cmd == "c":
            # List all classes, as specified earlier by the user
            for j, c in enumerate(classes):
                print "{0} : {1}".format(j, c)
        elif cmd == "s":
            # Move on to the next file.
            i = i + 1
        elif cmd.isdigit():
            # Add this label to TO_WRITE
            to_write.append([files[i], cmd, classes[int(cmd)]])
            i = i + 1

    # Write to CSV
    with open(output_file, 'w') as csvfile:
        write = csv.writer(csvfile)
        write.writerows(to_write)

if __name__ == "__main__":
    main()
