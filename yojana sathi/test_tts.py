from utils.tts import generate_speech

text = "नमस्ते! मैं योजना साथी हूँ। मैं आपको सरकारी योजनाओं की जानकारी देने में मदद कर सकता हूँ।"

try:
    output = generate_speech(text)

    print("TTS successful!")
    print("Audio saved at:", output)

except Exception as e:
    print("TTS Error:", e)