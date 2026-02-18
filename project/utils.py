# utils.py

import re
from datetime import datetime


def normalize_text(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def current_time():
    return datetime.now().strftime("%H:%M")


def current_date():
    return datetime.now().strftime("%d-%m-%Y")
