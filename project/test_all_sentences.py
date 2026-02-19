#!/usr/bin/env python3
# Test all 20 sentences for proper functionality

from hindi_chatbot import chatbot_reply

def test_all_20_sentences():
    print("🧪 Testing All 20 Hindi Sentences")
    print("=" * 60)
    
    sentences = [
        # 🕒 Time & Date Sentences
        ("अभी समय क्या है", "Time Query"),
        ("आज की तारीख बता दो", "Date Query"),
        ("आज कौन सा दिन है बताओ", "Day Query"),
        
        # 🌦 Weather Sentences
        ("आज का मौसम कैसा है", "Weather Query"),
        ("बाहर तापमान कितना है", "Temperature Query"),
        
        # 📍 Location Sentences
        ("मैं अभी कहाँ पर हूँ", "Location Query"),
        ("मेरा ठिकाना बता दो", "Place Query"),
        
        # 🏥 Local Information Sentences
        ("पास में अस्पताल कहाँ है", "Hospital Query"),
        ("यहाँ कोई मंदिर है क्या", "Temple Query"),
        ("बस स्टैंड किधर है", "Bus Stand Query"),
        
        # 🧠 Assistant Information Sentences
        ("तुम लोग कौन हो", "Identity Query"),
        ("तुम क्या काम कर सकते हो", "Capabilities Query"),
        ("मुझे मदद चाहिए", "Help Query"),
        
        # 🔊 System Control Sentences
        ("आवाज़ थोड़ी कम कर दो", "Volume Down"),
        ("आवाज़ थोड़ी बढ़ा दो", "Volume Up"),
        
        # 📴 Control Sentences
        ("अब शुरू करो जी", "Start Command"),
        ("काम बंद करो अब", "Stop Command"),
        
        # 🙏 Social Sentences
        ("नमस्ते दोस्त", "Greeting"),
        ("तुम्हारा बहुत धन्यवाद", "Thanks"),
        
        # 🎵 Voice Change Sentence
        ("आवाज़ बदल दो जी", "Voice Change")
    ]
    
    success_count = 0
    total_count = len(sentences)
    
    for i, (sentence, description) in enumerate(sentences, 1):
        try:
            response = chatbot_reply(sentence)
            print(f"\n{i:2d}. 📝 {description}")
            print(f"    🔊 Sentence: {sentence}")
            print(f"    💬 Response: {response}")
            
            # Check if response is meaningful (not fallback)
            if response != "माफ़ कीजिए, मैं यह समझ नहीं पाया":
                print(f"    ✅ Status: WORKING")
                success_count += 1
            else:
                print(f"    ❌ Status: NOT RECOGNIZED")
                
            print("-" * 50)
            
        except Exception as e:
            print(f"\n{i:2d}. ❌ ERROR with '{sentence}': {e}")
            print("-" * 50)
    
    # Summary
    print(f"\n🎯 TEST SUMMARY")
    print(f"✅ Working: {success_count}/{total_count}")
    print(f"❌ Failed: {total_count - success_count}/{total_count}")
    print(f"📊 Success Rate: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print("\n🎉 ALL 20 SENTENCES WORK PERFECTLY!")
    elif success_count >= 18:
        print("\n✅ EXCELLENT - 90%+ sentences working!")
    elif success_count >= 15:
        print("\n👍 GOOD - 75%+ sentences working!")
    else:
        print("\n⚠️ NEEDS IMPROVEMENT - Below 75% success rate")

if __name__ == "__main__":
    test_all_20_sentences()
