Directory structure:

for drum replacement:

/corpus             :   directory containing the original .WAV files

/separated_corpus   :   directory containing individual drum hits extracted 
                        from .WAV files in corpus

/corpus_mfcc.py     :   python script that takes in a directory, 
                        computes MFCC features for all the files inside the
                        directory, and spits out the output into a .csv file 

/separate_drums.py  :   extract individual drum hits from a directory of .WAV
                        files

/reconstruct.py     :   python script that takes in a .wav file and 
                        reconstructs it based on feature matching from a csv
                        file containing feature vectors, for example
                        corpus_mfcc.csv

How to use:
1.) Put all the original drum files in /corpus
2.) $ python separate_drums.py corpus separated_corpus
    This will clear separated_corpus, and then populate it with individual
    drum hits from all files in corpus. 
3.) $ python corpus_mfcc.py separated_corpus corpus_mfccs.csv
    Computes MFCC features on all files in separated_corpus and stores in a 
    csv file corpus_mfccs.csv
4.) $ python reconstruct.py input.wav corpus_mfccs.csv 
    Creates a file output.wav from reconstructing input.wav with samples 
    from corpus
    
for chroma analysis:

/midi_files         :   a directory for MIDI files

/wav_files          :   a directory for .WAV files used in training

/test_files         :   a directory for .WAV files used in testing

/chromagrams        :   a directory of chromagrams stored as numpy arrays
                        to be analyzed by the SVM

/midi_gen.py        :   script for generating MIDI files

/test_gen.py        :   script for generating testing .WAV files from MIDI
                        files

/train_gen.py       :   script for generating training .WAV files from MIDI
                        files

/chroma_extract.py  :   extract chromagram information from a directory of
                        .WAV files
                        
/svm_train.py       :   train and test the SVM on batches of chroma data

How to use:
(formal method still in development)
