#! /usr/bin/env python

import os, sys

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
output_dir = raw_input("--> Enter output directory : ")
while os.path.exists(output_dir):
    output_dir = raw_input("--> Error, directory/file already exists." +
                           " Enter output directory : ")
