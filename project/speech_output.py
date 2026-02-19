# speech_output.py
# Uses espeak-ng for offline Hindi TTS via temp file

import subprocess
import os
import tempfile

ENABLE_TTS = True
# Path to espeak-ng executable (adjust if installed elsewhere)
ESPEAK_PATH = r"C:\Program Files\eSpeak NG\espeak-ng.exe"
_TMP_FILE = os.path.join(tempfile.gettempdir(), "shruti_tts.txt")

# Voice configurations
VOICE_CONFIGS = {
    "male": {
        "voice": "hi",
        "pitch": 50,
        "speed": 150
    },
    "female": {
        "voice": "hi+f3",  # Higher pitch for female voice
        "pitch": 80,
        "speed": 160
    }
}

# Current voice preference (will be set by user)
current_voice = "male"

def set_voice_preference(gender):
    """Set the voice preference (male/female)"""
    global current_voice
    if gender.lower() in ["male", "female", "पुरुष", "महिला", "अॉरत", "लड़का", "लड़की"]:
        current_voice = "female" if gender.lower() in ["female", "महिला", "अॉरत", "लड़की"] else "male"
        return True
    return False

def get_available_voices():
    """Get list of available voice options"""
    return ["male", "female"]

def speak(text):
    if not ENABLE_TTS:
        return
    try:
        # Write text to temp file with UTF-8 encoding
        with open(_TMP_FILE, "w", encoding="utf-8") as f:
            f.write(text)
            
        # Get voice configuration
        voice_config = VOICE_CONFIGS[current_voice]
        
        # Call espeak-ng with gender-specific parameters
        subprocess.call([
            ESPEAK_PATH,
            "-v", voice_config["voice"],      # Voice variant
            "-p", str(voice_config["pitch"]),  # Pitch adjustment
            "-s", str(voice_config["speed"]),  # Speed
            "-f", _TMP_FILE  # Read from file
        ])
    except Exception as e:
        print(f"TTS Error: {e}")
