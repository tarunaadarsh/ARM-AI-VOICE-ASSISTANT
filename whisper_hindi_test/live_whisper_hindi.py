import sounddevice as sd
import numpy as np
import whisper
import time
from datetime import datetime
import sys

# ================== CONFIG ==================
DEVICE_INDEX = 9            # Your microphone device
SAMPLE_RATE = 48000         # MUST match mic default
CHANNELS = 1
RECORD_SECONDS = 4          # Each speech chunk
SILENCE_THRESHOLD = 0.01    # Adjust if needed
MODEL_SIZE = "small"        # tiny / base / small
STOP_WORDS = ["बंद", "रुको", "stop"]

# Local static info (offline)
LOCATION = "कुन्द्रथुर, चेन्नई"
TEMPERATURE = "32°C"
WEATHER = "धूप"
# ============================================

print("📦 Loading Whisper Model...")
model = whisper.load_model(MODEL_SIZE)

print("\n🎤 LIVE HINDI VOICE ASSISTANT")
print("🛑 CTRL + C दबाकर बंद करें\n")


def record_audio():
    """Record fixed-duration audio chunk"""
    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        device=DEVICE_INDEX
    )
    sd.wait()
    return audio.flatten()


def is_silence(audio):
    """Detect silence to avoid useless inference"""
    return np.max(np.abs(audio)) < SILENCE_THRESHOLD


def chatbot_reply(text):
    text = text.strip()

    # EXIT
    if any(w in text for w in STOP_WORDS):
        return "ठीक है, मैं बंद हो रहा हूँ", True

    # TIME
    if any(w in text for w in ["समय", "टाइम", "clock"]):
        now = datetime.now().strftime("%H:%M")
        return f"अभी समय {now} है", False

    # DATE
    if any(w in text for w in ["तारीख", "दिन", "डेट"]):
        today = datetime.now().strftime("%d-%m-%Y")
        return f"आज की तारीख {today} है", False

    # LOCATION
    if any(w in text for w in ["मैं कहाँ", "मेरी जगह", "लोकेशन"]):
        return f"आप {LOCATION} में हैं", False

    # WEATHER
    if "मौसम" in text or "तापमान" in text:
        return f"{LOCATION} में तापमान {TEMPERATURE} है और मौसम {WEATHER} है", False

    # IDENTITY
    if any(w in text for w in ["तुम कौन", "आप कौन", "तुम क्या हो"]):
        return "मैं एक ऑफलाइन हिंदी वॉइस असिस्टेंट हूँ, पूरी तरह प्राइवेट", False

    # HELP
    if "मदद" in text or "क्या कर सकते" in text:
        return (
            "मैं समय, तारीख, मौसम, लोकेशन और स्थानीय जानकारी बता सकता हूँ",
            False
        )

    return "माफ़ कीजिए, मैं यह समझ नहीं पाया", False


# ================== MAIN LOOP ==================
try:
    while True:
        print("🎙️ Listening...")
        audio = record_audio()

        if is_silence(audio):
            print("🤫 Silence detected, skipping...\n")
            continue

        result = model.transcribe(
            audio,
            language="hi",
            fp16=False
        )

        text = result["text"].strip()

        if not text:
            print("🤫 Empty speech\n")
            continue

        print(f"🧑 User : {text}")

        reply, should_exit = chatbot_reply(text)
        print(f"🤖 Bot  : {reply}\n")

        if should_exit:
            break

except KeyboardInterrupt:
    print("\n🛑 Assistant interrupted by user")

finally:
    print("✅ Assistant stopped safely")
    sys.exit(0)
