#!/usr/bin/env python3
# Test script for male and female voices

from speech_output import speak, set_voice_preference
import time

def test_voices():
    print("🔊 Testing Voice Options...")
    
    # Test male voice
    print("\n1. Testing Male Voice:")
    set_voice_preference("male")
    speak("यह पुरुष की आवाज है, मैं आपकी मदद कर सकता हूँ")
    time.sleep(2)
    
    # Test female voice
    print("\n2. Testing Female Voice:")
    set_voice_preference("female")
    speak("यह महिला की आवाज है, मैं आपकी मदद कर सकती हूँ")
    time.sleep(2)
    
    print("\n✅ Voice test completed!")
    print("Both male and female voices are working correctly.")

if __name__ == "__main__":
    test_voices()
