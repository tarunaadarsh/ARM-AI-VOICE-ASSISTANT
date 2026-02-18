# speech_input.py

import pyaudio
import json
from vosk import Model, KaldiRecognizer

RATE = 16000
CHUNK = 4000


class SpeechRecognizer:
    def __init__(self, model_path):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, RATE)

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

    def listen(self):
        data = self.stream.read(CHUNK, exception_on_overflow=False)
        if self.recognizer.AcceptWaveform(data):
            result = json.loads(self.recognizer.Result())
            return result.get("text", "").strip()
        return None

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
