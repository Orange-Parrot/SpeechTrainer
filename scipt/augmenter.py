'''
This script is meant to augment the inputted wav files into ~2000 variation of pitches and noise output.

Current stage: testing pitch manupulation
Source: https://stackoverflow.com/questions/43963982/python-change-pitch-of-wav-file#43964107
'''

import wave
import numpy as np

wr = wave.open('../assets/hello/wav/hello1.wav', 'r')
# Set the parameters for the output file.
par = list(wr.getparams())

print('sample set from', par[3], 'to 0')
par[3] = 0  # The number of samples will be set by writeframes.
par = tuple(par)
# initing the output file
ww = wave.open('output1.wav', 'w')
ww.setparams(par)

# fr = reverb
fr = 20
sz = wr.getframerate()//fr  # Read and process 1/fr second at a time.
# A larger number for fr means less reverb.
c = int(wr.getnframes()/sz)  # count of the whole file
shift = 100//fr  # shifting 100 Hz. ACTUAL FREQUENCY MANUPULATOR
for num in range(c):
    # Read the data, split it in left and right channel (assuming a stereo WAV file).
    da = np.fromstring(wr.readframes(sz), dtype=np.int16)
    left, right = da[0::2], da[1::2]  # left and right channel
    # Extract the frequencies using the Fast Fourier Transform built into numpy.
    lf, rf = np.fft.rfft(left), np.fft.rfft(right)
    # Roll the array to increase the pitch.
    lf, rf = np.roll(lf, shift), np.roll(rf, shift)
    # The highest frequencies roll over to the lowest ones. That's not what we want, so zero them.
    lf[0:shift], rf[0:shift] = 0, 0
    # Now use the inverse Fourier transform to convert the signal back into amplitude.
    nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
    # Combine the two channels.
    ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
    # Write the output data.
    ww.writeframes(ns.tostring())

wr.close()
ww.close()