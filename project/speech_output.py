# speech_output.py

import subprocess

ENABLE_TTS = True


def speak(text):
    if not ENABLE_TTS:
        return
    try:
        subprocess.call([
            "espeak-ng",
            "-v", "hi",
            "-s", "150",
            text
        ])
    except Exception:
        pass
