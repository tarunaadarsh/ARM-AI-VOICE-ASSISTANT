#!/usr/bin/env python3
# Test script for all new Hindi voice commands

from hindi_chatbot import chatbot_reply

def test_all_commands():
    print("🧪 Testing All New Hindi Voice Commands")
    print("=" * 50)
    
    commands = [
        # 🕒 Time & Date
        ("समय क्या है", "Time Query"),
        ("आज की तारीख क्या है", "Date Query"),
        ("आज कौन सा दिन है", "Day Query"),
        
        # 🌦 Weather
        ("आज का मौसम बताओ", "Weather Query"),
        ("तापमान कितना है", "Temperature Query"),
        
        # 📍 Location
        ("मैं कहाँ हूँ", "Location Query"),
        ("मेरी जगह बताओ", "Place Query"),
        
        # 🏥 Local Info
        ("नज़दीकी अस्पताल", "Hospital Query"),
        ("नज़दीकी मंदिर", "Temple Query"),
        ("बस स्टैंड कहाँ है", "Bus Stand Query"),
        
        # 🧠 Assistant
        ("तुम कौन हो", "Identity Query"),
        ("तुम क्या कर सकते हो", "Capabilities Query"),
        ("मदद करो", "Help Query"),
        
        # 🔊 System
        ("आवाज़ कम करो", "Volume Down"),
        ("आवाज़ बढ़ाओ", "Volume Up"),
        
        # 📴 Control
        ("शुरू करो", "Start Command"),
        
        # Extra
        ("समाचार बताओ", "News Query"),
        ("आज की सुर्खियाँ", "Headlines Query"),
        ("धन्यवाद", "Thanks"),
    ]
    
    for command, description in commands:
        response = chatbot_reply(command)
        print(f"\n📝 {description}")
        print(f"🔊 Command: {command}")
        print(f"💬 Response: {response}")
        print("-" * 40)
    
    print("\n✅ All commands tested successfully!")

if __name__ == "__main__":
    test_all_commands()
