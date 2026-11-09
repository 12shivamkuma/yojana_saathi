from utils.retriever import find_schemes
from utils.response import generate_response
from utils.tts import generate_speech

# 1. User query
query = "मुझे खेती के लिए सरकारी सहायता चाहिए"

# 2. Find relevant scheme
schemes = find_schemes(query)

# 3. Generate Hindi response
answer = generate_response(query, schemes)

print("\n----- YOJANA SAATHI RESPONSE -----")
print(answer)

# 4. Convert response into speech
print("\nGenerating audio...")

try:
    audio_path = generate_speech(
        answer,
        output_path="audio/response.wav"
    )

    print("Audio generated successfully!")
    print("Saved at:", audio_path)

except Exception as e:
    print("TTS Error:", e)