import streamlit as st
import os
from dotenv import load_dotenv
from gnani.tts import GnaniTTSClient, AudioConfig

load_dotenv()

GNANI_API_KEY = os.getenv("GNANI_API_KEY")

if not GNANI_API_KEY:
    try:
        GNANI_API_KEY = st.secrets["GNANI_API_KEY"]
    except Exception:
        GNANI_API_KEY = None

def generate_speech(text, output_path="audio/response.wav"):

    if not API_KEY:
        raise ValueError("Gnani API key not found.")

    client = GnaniTTSClient(api_key=API_KEY)

    audio = client.synthesize(
        text,
        voice="Shivani",
        model="timbre-v3.0",
        audio_config=AudioConfig(
            sample_rate=48000,
            encoding="linear_pcm",
            container="wav"
        )
    )

    with open(output_path, "wb") as f:
        f.write(audio)

    return output_path
