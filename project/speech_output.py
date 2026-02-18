# speech_output.py
# Uses espeak-ng for offline Hindi TTS via temp file

import subprocess
import os
import tempfile

ENABLE_TTS = True
# Path to espeak-ng executable (adjust if installed elsewhere)
ESPEAK_PATH = r"C:\Program Files\eSpeak NG\espeak-ng.exe"
_TMP_FILE = os.path.join(tempfile.gettempdir(), "shruti_tts.txt")

def speak(text):
    if not ENABLE_TTS:
        return
    try:
        # Write text to temp file with UTF-8 encoding
        with open(_TMP_FILE, "w", encoding="utf-8") as f:
            f.write(text)
            
        # Call espeak-ng pointing to the file
        subprocess.call([
            ESPEAK_PATH,
            "-v", "hi",      # Hindi voice
            "-s", "150",     # Speed
            "-f", _TMP_FILE  # Read from file
        ])
    except Exception as e:
        print(f"TTS Error: {e}")
