# intents.py

STOP_WORD = "बंद"

INTENTS = {
    "TIME": ["समय", "टाइम", "time"],
    "DATE": ["तारीख", "दिन", "डेट", "date"],
    "WEATHER": ["मौसम", "तापमान", "weather"],
    "LOCATION": ["कहाँ", "कहा", "किधर", "स्थान", "जगह"],
    "LANDMARK": ["नज़दीकी", "पास", "लैंडमार्क"],
    "EMERGENCY": ["पुलिस", "एम्बुलेंस", "आग"],
    "IDENTITY": ["तुम कौन", "आप कौन", "क्या हो"],
    "NAME": ["नाम क्या", "तुम्हारा नाम"],
    "HELP": ["मदद", "help"],
    "STOP": [STOP_WORD]
}


def detect_intent(text):
    for intent, keywords in INTENTS.items():
        for word in keywords:
            if word in text:
                return intent
    return "UNKNOWN"
