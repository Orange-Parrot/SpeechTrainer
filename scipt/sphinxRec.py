# BETA TESTING
import os
from pocketsphinx import AudioFile, get_model_path, get_data_path

model_path = get_model_path()
# data_path = get_data_path()
data_path = "../assets/hello/wav/altered/"
print(data_path)

config = {
    'verbose': False,
    'audio_file': os.path.join(data_path, 'uh.wav'),
    'buffer_size': 2048,
    'no_search': False,
    'full_utt': False,
    'hmm': os.path.join(model_path, 'en-us'),
    'lm': os.path.join(model_path, 'en-us.lm.bin'),
    'dict': os.path.join("model/", '1800.dict')
}

audio = AudioFile(**config)
for phrase in audio:
    print(phrase)

# the amount of stutter detected
print(len(audio))