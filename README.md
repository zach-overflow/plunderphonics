plunderphonics
==============
The end goal of plunderphonics is to create a new song from samples of other songs using machine learning algorithms.

 At the moment we are working on classifying individual drum hits from an audio clip of any drum solo. These clips will be compared against a large collection of stock drum samples in order to determine what sample sounds most similar to each individual drum hit.
 
 We are also developing tools for chord recognition using chroma analysis and note-to-chord matching.

currently we only support wav files.

requirements:
- aubio: http://aubio.org/
- wavio: https://gist.github.com/WarrenWeckesser/7461781
- librosa: https://github.com/bmcfee/librosa/
- pyaudio: http://people.csail.mit.edu/hubert/pyaudio/
