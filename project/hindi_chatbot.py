import pyaudio
import json
import subprocess
import re
from vosk import Model, KaldiRecognizer
from datetime import datetime

# ================= CONFIG =================
RATE = 16000
CHUNK = 4000
MODEL_PATH = "vosk-model-small-hi-0.22"
STOP_WORD = "बंद"

# ================= LOCAL DATA =================
LOCAL_PROFILE = {
    "area": "कुन्द्रथुर",
    "city": "चेन्नई",
    "state": "तमिलनाडु"
}

LOCAL_WEATHER = {
    "temperature": "32°C",
    "condition": "धूप",
    "humidity": "60%"
}

LOCAL_LANDMARKS = [
    "कुन्द्रथुर मुरुगन मंदिर",
    "मंगडु",
    "पोरुर",
    "मदनंदपुरम",
    "श्री रामचंद्र अस्पताल"
]

EMERGENCY_NUMBERS = {
    "पुलिस": "100",
    "एम्बुलेंस": "108",
    "आग": "101"
}

# ================= TTS =================
def speak(text):
    try:
        subprocess.call(["espeak-ng", "-v", "hi", "-s", "150", text])
    except:
        pass

# ================= UTILS =================
def normalize(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

# ================= INTENT LOGIC =================
def chatbot_reply(text):
    text = normalize(text)

    # ---- STOP ----
    if STOP_WORD in text or "रुक" in text or "बंद करो" in text:
        return "ठीक है, मैं बंद हो रहा हूँ"

    # ---- TIME ----
    if any(w in text for w in [
        "समय", "टाइम", "कितना बजा", "घड़ी", "time"
    ]):
        now = datetime.now().strftime("%H:%M")
        return f"अभी समय {now} है"

    # ---- DATE ----
    if any(w in text for w in [
        "तारीख", "दिन", "डेट", "date", "आज कौन सा दिन"
    ]):
        today = datetime.now().strftime("%d-%m-%Y")
        return f"आज की तारीख {today} है"

    # ---- WEATHER ----
    if any(w in text for w in [
        "मौसम", "तापमान", "weather", "गर्मी", "बारिश"
    ]):
        return (
            f"{LOCAL_PROFILE['area']} में तापमान "
            f"{LOCAL_WEATHER['temperature']} है और "
            f"मौसम {LOCAL_WEATHER['condition']} है"
        )

    # ---- LOCATION ----
    if any(w in text for w in [
        "मैं कहाँ", "कहा हूँ", "लोकेशन", "स्थान", "जगह"
    ]):
        return (
            f"आप {LOCAL_PROFILE['area']}, "
            f"{LOCAL_PROFILE['city']} में हैं"
        )

    # ---- LANDMARKS ----
    if any(w in text for w in [
        "नज़दीकी", "पास", "लैंडमार्क", "आसपास"
    ]):
        return "नज़दीकी स्थान हैं: " + ", ".join(LOCAL_LANDMARKS)

    # ---- EMERGENCY ----
    for key in EMERGENCY_NUMBERS:
        if key in text:
            return f"{key} का नंबर {EMERGENCY_NUMBERS[key]} है"

    # ---- IDENTITY ----
    if any(w in text for w in [
        "तुम कौन", "आप कौन", "क्या हो", "कौन हो"
    ]):
        return (
            "मैं एक पूरी तरह ऑफलाइन हिंदी वॉइस असिस्टेंट हूँ "
            "जो आपकी प्राइवेसी का सम्मान करता है"
        )

    # ---- NAME ----
    if any(w in text for w in [
        "नाम क्या", "तुम्हारा नाम", "आपका नाम"
    ]):
        return "मेरा नाम कुन्द्रथुर हिंदी वॉइस असिस्टेंट है"

    # ---- HELP ----
    if any(w in text for w in [
        "मदद", "help", "क्या कर सकते", "क्षमता"
    ]):
        return (
            "मैं समय, तारीख, मौसम, लोकेशन, "
            "नज़दीकी स्थान और आपातकालीन जानकारी दे सकता हूँ"
        )

    # ---- GREETINGS ----
    if any(w in text for w in [
        "नमस्ते", "हेलो", "सुप्रभात", "शुभ संध्या"
    ]):
        return "नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ"

    # ---- THANKS ----
    if any(w in text for w in [
        "धन्यवाद", "शुक्रिया", "थैंक यू"
    ]):
        return "आपका स्वागत है"

    # ---- FALLBACK ----
    return "माफ़ कीजिए, मैं यह समझ नहीं पाया"

# ================= MAIN =================
print("🔁 Kundrathur Hindi Voice Assistant Starting...")
print("📦 Loading Hindi Vosk Model...")

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, RATE)

audio = pyaudio.PyAudio()
stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

print("🎤 बोलिए (Speak in Hindi)")
print(f"❌ '{STOP_WORD}' बोलकर बंद करें\n")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            user_text = result.get("text", "").strip()

            if user_text:
                print(f"\n🧑 User : {user_text}")
                reply = chatbot_reply(user_text)
                print(f"🤖 Bot  : {reply}")
                speak(reply)

                if STOP_WORD in user_text:
                    break

except KeyboardInterrupt:
    print("\n🛑 Program interrupted")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("✅ Assistant stopped")
