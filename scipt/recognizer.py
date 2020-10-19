import speech_recognition as sr
import os
from pydub import AudioSegment, effects
from pydub.silence import  split_on_silence
import time

AUDIO_FILE = "../assets/hello/wav/altered/templateSpeech.wav"
lang = "en-US"
noise_sample_duration = 1 # unit = s

############################## AUDIO PREPROCESSING
# normalize audio
def match_target_amplitude(sound, target_dBFS):
  change_in_dBFS = target_dBFS - sound.dBFS
  return sound.apply_gain(change_in_dBFS)

raw = AudioSegment.from_wav(AUDIO_FILE)
norm = match_target_amplitude(raw, -20.0)
audio_tag = id(norm)
try:
  os.mkdir(".temp")
except(FileExistsError):
  pass
NORM_PATH = "./.temp/chunk{id}.wav".format(id=audio_tag)
norm.export(NORM_PATH, format="wav")
print("[info] Audio successfully preprocessed")
############################## AUDIO PREPROCESSING

def detect(audio_path, phrases=[]):
  with sr.AudioFile(audio_path) as source:
    # reads the audio file. Here we use record instead of listen
    audio = r.record(source)
    r.adjust_for_ambient_noise(source, duration=noise_sample_duration) # adjust to ambient noise sampled 3 seconds (program dependant)
    print("[info] Threshold successfully adjusted")

  print("[info] Audio loaded")
  result = ""

  # debug purpose only
  start = time.time()

  print("[info] Recognizing..")

  try:
    result = r.recognize_google(audio, language=lang)
    print("[info] Successfully recognized audio!")
  except sr.UnknownValueError:
    print("[error] Cannot recognize or understand audio")
  except sr.RequestError as e:
    print("[error] Google error; {0}".format(e))

  end = time.time()
  print("[debug] Recognition took {time} seconds".format(time=end-start))

  stutter_list = {}
  for i in phrases:
    total_nums = 0
    location = []
    word_position = 0
    for j in result.split():
      if j == i:
        total_nums += 1
        location.append(word_position)
      word_position += 1
    stutter_list[i] = [total_nums, location]

  return result, stutter_list, True if '*' in result else False

# init recognizer
r = sr.Recognizer()
# set energy threshold
r.dynamic_energy_threshold = True #dynamic threshold for better performance
text, detections, contain_curses = detect(NORM_PATH, ['so', 'was'])
print("[prediction] words detected =", detections)
# print("[prediction] Recognized text: \n{tag}".format(tag=text))
print("[prediction] Contains naughty words = {curse}".format(curse=contain_curses))

# flush and clean temporary normalized file
try:
  os.remove(NORM_PATH)
except(FileNotFoundError):
  print("Failed to locate normalized audio")