from utils.stt import transcribe_audio

audio_path = "audio/test_hindi.wav"

try:
    transcript = transcribe_audio(audio_path)

    print("\n----- GNANI PRISMA RESULT -----")
    print("Transcript:", transcript)

except Exception as e:
    print("Error:", e)