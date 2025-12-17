import sys
import os
import json
from PIL import ImageGrab
import google.generativeai as genai

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from knowledge_interface import KnowledgeInterface

def test_api():
    print(">>> Testing Gemini API Key Configuration <<<")
    
    ki = KnowledgeInterface()
    config = ki.config
    api_key = config.get("api_keys", {}).get("gemini", "")
    
    if not api_key:
        print("❌ API Key not found in configuration.")
        return

    print(f"✅ API Key found: {api_key[:5]}...{api_key[-5:]}")
    
    # Test API call
    try:
        print(">>> Listing available models...")
        genai.configure(api_key=api_key)
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
        
        print(">>> Attempting to call Gemini API with 'gemini-2.5-flash-native-audio-dialog'...")
        model = genai.GenerativeModel('gemini-2.5-flash-native-audio-dialog')
        
        response = model.generate_content("Hello, are you working? Please reply with 'Yes, I am active.'")
        print(f"✅ API Response: {response.text}")
        
    except Exception as e:
        print(f"❌ API Call Failed: {e}")

if __name__ == "__main__":
    test_api()
