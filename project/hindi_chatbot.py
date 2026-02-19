import pyaudio
import json
import subprocess
import re
from vosk import Model, KaldiRecognizer
from datetime import datetime
from speech_output import speak, set_voice_preference, get_available_voices

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
    "श्री रामचंद्र अस्पताल",
    "कुन्द्रथुर बस स्टैंड",
    "कुन्द्रथुर सरकारी अस्पताल",
    "श्री पेरुमल मंदिर"
]

EMERGENCY_NUMBERS = {
    "पुलिस": "100",
    "एम्बुलेंस": "108",
    "आग": "101"
}

# Voice volume control
voice_volume = 100  # Default volume

# ================= INTENT DEFINITIONS =================
# हिंदी कमांड के विभिन्न रूप (Hindi command variations)

TIME_INTENT = [
    "अभी समय क्या है", "इस समय कितने बजे हैं", 
    "मुझे अभी का समय बताओ", "समय बताओ",
    "समय क्या है", "कितना बजा", "घड़ी", "time"
]

DATE_INTENT = [
    "आज की तारीख क्या है", "आज की पूरी तारीख बताओ",
    "आज दिन और तारीख क्या है", "आज कौन सा दिन है",
    "तारीख", "दिन", "डेट", "date", "आज कौन सा दिन"
]

WEATHER_INTENT = [
    "आज का मौसम कैसा है", "आज मौसम की जानकारी दो",
    "आज तापमान कितना है", "यहाँ का तापमान बताओ",
    "तापमान कितना है", "मौसम", "तापमान", "weather", 
    "गर्मी", "बारिश", "आज का मौसम बताओ"
]

LOCATION_INTENT = [
    "मैं कहाँ हूँ", "मेरी लोकेशन क्या है",
    "मेरी वर्तमान जगह बताओ", "अभी मैं किस स्थान पर हूँ",
    "मैं कहाँ", "कहा हूँ", "लोकेशन", "स्थान", "जगह",
    "मेरी जगह बताओ", "मैं अभी कहाँ पर हूँ", "मेरा ठिकाना बता दो"
]

HOSPITAL_INTENT = [
    "नज़दीकी अस्पताल बताओ", "पास में कौन सा अस्पताल है",
    "सबसे पास का अस्पताल कौन सा है", "नज़दीकी अस्पताल", 
    "अस्पताल", "hospital"
]

BUS_STAND_INTENT = [
    "बस स्टैंड कहाँ है", "नज़दीकी बस स्टैंड बताओ",
    "यहाँ का बस स्टैंड कौन सा है", "बस स्टैंड",
    "बस स्टैंड किधर है", "bus stand"
]

IDENTITY_INTENT = [
    "तुम कौन हो", "आप कौन हैं", "तुम्हारा नाम क्या है",
    "तुम कौन", "आप कौन", "क्या हो", "कौन हो", "तुम कौन हो"
]

VOLUME_DOWN_INTENT = [
    "आवाज़ कम करो", "वॉल्यूम कम करो", "आवाज कम",
    "volume kam", "कम आवाज", "आवाज़ थोड़ी कम कर दो"
]

VOLUME_UP_INTENT = [
    "आवाज़ बढ़ाओ", "वॉल्यूम बढ़ा दो", "आवाज बढ़ा",
    "volume badhao", "ज़ोर आवाज", "आवाज़ थोड़ी बढ़ा दो"
]

START_INTENT = [
    "शुरू करो", "चालू हो जाओ", "start", "शुरू", "चालू करो",
    "अब शुरू करो जी"
]

STOP_INTENT = [
    "बंद हो जाओ", "रुक जाओ", STOP_WORD, "रुक", "बंद करो"
]

HELP_INTENT = [
    "मदद करो", "मेरी सहायता करो", "help", "मदद",
    "मदद करो", "क्या कर सकते"
]

# Temple and other existing intents remain the same
TEMPLE_INTENT = ["नज़दीकी मंदिर", "मंदिर", "temple"]
GENERAL_LANDMARK_INTENT = ["नज़दीकी", "पास", "लैंडमार्क", "आसपास"]
EMERGENCY_INTENT = list(EMERGENCY_NUMBERS.keys())
GREETING_INTENT = ["नमस्ते", "हेलो", "सुप्रभात", "शुभ संध्या"]
THANKS_INTENT = ["धन्यवाद", "शुक्रिया", "थैंक यू"]
VOICE_CHANGE_INTENT = [
    "आवाज बदलो", "voice change", "आवाज बदलिए", 
    "voice badlo", "आवाज़ बदल दो जी"
]
NEWS_INTENT = ["समाचार बताओ", "न्यूज़", "खबरें", "samachar"]
HEADLINES_INTENT = ["आज की सुर्खियाँ", "सुर्खियाँ", "headlines"]
NAME_INTENT = ["नाम क्या", "तुम्हारा नाम", "आपका नाम"]

# ================= GENDER SELECTION =================
def select_voice_gender():
    """Ask user to select voice gender preference"""
    print("\n🎵 Voice Selection")
    print("1. Male Voice (पुरुष आवाज)")
    print("2. Female Voice (महिला आवाज)")
    print("3. Hear samples (नमूने सुनें)")
    
    while True:
        try:
            choice = input("\nSelect voice option (1/2/3): ").strip()
            
            if choice == "1":
                set_voice_preference("male")
                speak("मैं अब पुरुष की आवाज में बोलूंगा")
                print("✅ Male voice selected")
                return "male"
                
            elif choice == "2":
                set_voice_preference("female")
                speak("मैं अब महिला की आवाज में बोलूंगी")
                print("✅ Female voice selected")
                return "female"
                
            elif choice == "3":
                print("\n🔊 Playing voice samples...")
                # Test male voice
                set_voice_preference("male")
                print("Playing male voice sample...")
                speak("यह पुरुष की आवाज है")
                
                # Test female voice
                set_voice_preference("female")
                print("Playing female voice sample...")
                speak("यह महिला की आवाज है")
                
                # Reset to male for selection
                set_voice_preference("male")
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3")
                
        except KeyboardInterrupt:
            print("\nUsing default male voice")
            set_voice_preference("male")
            return "male"

# ================= UTILS =================
def normalize(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

# ================= INTENT LOGIC =================
def chatbot_reply(text):
    text = normalize(text)
    global voice_volume

    # बंद करने का इरादा (Stop intent) - पहले चेक करें
    if any(phrase in text for phrase in STOP_INTENT):
        return "ठीक है, मैं बंद हो रहा हूँ"

    # ⏰ समय पूछना (Time query)
    if any(phrase in text for phrase in TIME_INTENT):
        now = datetime.now().strftime("%H:%M")
        return f"अभी समय {now} है"

    # 📅 तारीख पूछना (Date query)
    if any(phrase in text for phrase in DATE_INTENT):
        today = datetime.now().strftime("%d-%m-%Y")
        day_name = datetime.now().strftime("%A")
        return f"आज की तारीख {today} है और आज {day_name} है"

    # 🌤️ मौसम पूछना (Weather query)
    if any(phrase in text for phrase in WEATHER_INTENT):
        return (
            f"{LOCAL_PROFILE['area']} में तापमान "
            f"{LOCAL_WEATHER['temperature']} है और "
            f"मौसम {LOCAL_WEATHER['condition']} है"
        )

    # 📍 लोकेशन पूछना (Location query)
    if any(phrase in text for phrase in LOCATION_INTENT):
        return (
            f"आप {LOCAL_PROFILE['area']}, "
            f"{LOCAL_PROFILE['city']} में हैं"
        )

    # 🏥 अस्पताल की जानकारी (Hospital information)
    if any(phrase in text for phrase in HOSPITAL_INTENT):
        hospitals = [landmark for landmark in LOCAL_LANDMARKS if "अस्पताल" in landmark]
        return f"नज़दीकी अस्पताल हैं: " + ", ".join(hospitals) if hospitals else "नज़दीकी कोई अस्पताल नहीं मिला"

    # 🛕 मंदिर की जानकारी (Temple information)
    if any(phrase in text for phrase in TEMPLE_INTENT):
        temples = [landmark for landmark in LOCAL_LANDMARKS if "मंदिर" in landmark]
        return f"नज़दीकी मंदिर हैं: " + ", ".join(temples) if temples else "नज़दीकी कोई मंदिर नहीं मिला"

    # 🚌 बस स्टैंड की जानकारी (Bus stand information)
    if any(phrase in text for phrase in BUS_STAND_INTENT):
        bus_stands = [landmark for landmark in LOCAL_LANDMARKS if "बस स्टैंड" in landmark]
        return f"बस स्टैंड है: " + ", ".join(bus_stands) if bus_stands else "नज़दीकी कोई बस स्टैंड नहीं मिला"

    # 🏛️ सामान्य स्थान (General landmarks)
    if any(phrase in text for phrase in GENERAL_LANDMARK_INTENT):
        return "नज़दीकी स्थान हैं: " + ", ".join(LOCAL_LANDMARKS)

    # 🚨 आपातकालीन सेवाएँ (Emergency services)
    for key in EMERGENCY_INTENT:
        if key in text:
            return f"{key} का नंबर {EMERGENCY_NUMBERS[key]} है"

    # 🤖 सहायक की पहचान (Assistant identity)
    if any(phrase in text for phrase in IDENTITY_INTENT):
        return (
            "मैं एक पूरी तरह ऑफलाइन हिंदी वॉइस असिस्टेंट हूँ "
            "जो आपकी प्राइवेसी का सम्मान करता है"
        )

    # 💪 क्षमताएँ (Capabilities)
    if any(phrase in text for phrase in NAME_INTENT):
        return "मेरा नाम कुन्द्रथुर हिंदी वॉइस असिस्टेंट है"

    # 💪 क्षमताएँ (Capabilities)
    if any(phrase in text for phrase in HELP_INTENT):
        return (
            "मैं समय, तारीख, मौसम, लोकेशन, "
            "नज़दीकी स्थान और आपातकालीन जानकारी दे सकता हूँ"
        )

    # 🔊 आवाज़ कम करना (Volume down)
    if any(phrase in text for phrase in VOLUME_DOWN_INTENT):
        voice_volume = max(50, voice_volume - 20)
        return f"आवाज़ कम कर दी गई है, अब वॉल्यूम {voice_volume} है"

    # 🔊 आवाज़ बढ़ाना (Volume up)
    if any(phrase in text for phrase in VOLUME_UP_INTENT):
        voice_volume = min(150, voice_volume + 20)
        return f"आवाज़ बढ़ा दी गई है, अब वॉल्यूम {voice_volume} है"

    # 🚀 शुरू करना (Start command)
    if any(phrase in text for phrase in START_INTENT):
        return "मैं पहले से ही चालू हूँ, आपकी क्या मदद कर सकता हूँ?"

    # 📰 समाचार (News)
    if any(phrase in text for phrase in NEWS_INTENT):
        return "मैं ऑफलाइन हूँ, इसलिए अभी समाचार नहीं दे सकता। कृपया इंटरनेट कनेक्शन जांचें।"

    # 📰 सुर्खियाँ (Headlines)
    if any(phrase in text for phrase in HEADLINES_INTENT):
        return "मैं ऑफलाइन हूँ, इसलिए आज की सुर्खियाँ नहीं दे सकता। कृपया इंटरनेट कनेक्शन जांचें।"

    # 🙏 अभिवादन (Greetings)
    if any(phrase in text for phrase in GREETING_INTENT):
        return "नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ"

    # 🙏 धन्यवाद (Thanks)
    if any(phrase in text for phrase in THANKS_INTENT):
        return "आपका स्वागत है"

    # 🎵 आवाज़ बदलना (Voice change)
    if any(phrase in text for phrase in VOICE_CHANGE_INTENT):
        current_voice = "female" if selected_gender == "male" else "male"
        set_voice_preference(current_voice)
        return f"अब मैं {'महिला' if current_voice == 'female' else 'पुरुष'} की आवाज में बोलूंगा"

    # ❌ डिफ़ॉल्ट जवाब (Default response)
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

# Voice gender selection
selected_gender = select_voice_gender()

print(f"\n🎤 बोलिए (Speak in Hindi) - {selected_gender.title()} Voice Active")
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

                # Pause mic stream so speaker can output audio
                stream.stop_stream()
                speak(reply)
                # Resume mic stream after speaking
                stream.start_stream()

                if STOP_WORD in user_text:
                    break

except KeyboardInterrupt:
    print("\n🛑 Program interrupted")

finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("✅ Assistant stopped")
