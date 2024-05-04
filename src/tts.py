from dotenv import load_dotenv

from deepgram import (
    SpeakOptions,
)
from src.deepgram_client import deepgram_client

load_dotenv()

import sounddevice as sd
import soundfile as sf


DEEPGRAM_RESPONSE_SAMPLE_RATE = 24000

options = SpeakOptions(
    model="aura-asteria-en",
    encoding="linear16",
    container="wav"
)

def tts(txt, filename="last.wav"):
    try:
        speak_opts = {"text": txt}

        deepgram_client.speak.v("1").save(filename, speak_opts, options)
    except Exception as e:
        print(f"Exception: {e}")

def play(filename="last.wav"):
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)
    sd.wait()
