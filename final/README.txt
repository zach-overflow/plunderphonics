Directory structure:

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
