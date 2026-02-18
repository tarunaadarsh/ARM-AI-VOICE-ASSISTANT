from datetime import datetime

def answer_local_query(text):
    text = text.lower()

    if "समय" in text or "time" in text:
        return f"अभी समय है {datetime.now().strftime('%H:%M')}"

    if "तारीख" in text or "date" in text:
        return f"आज की तारीख है {datetime.now().strftime('%d-%m-%Y')}"

    if "तुम्हारा नाम" in text:
        return "मेरा नाम लोकल हिंदी वॉइस असिस्टेंट है"

    if "मेरा नाम" in text:
        return "आपने अभी अपना नाम नहीं बताया"

    if "भारत" in text and "राजधानी" in text:
        return "भारत की राजधानी नई दिल्ली है"

    if "नमस्ते" in text or "hello" in text:
        return "नमस्ते! मैं आपकी कैसे मदद कर सकता हूँ?"

    return None
