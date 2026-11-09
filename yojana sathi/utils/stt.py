import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GNANI_API_KEY = os.getenv("GNANI_API_KEY")
print("API key loaded:", bool(GNANI_API_KEY))
print("API key length:", len(GNANI_API_KEY) if GNANI_API_KEY else 0)

STT_URL = "https://api.vachana.ai/stt/v3"


def transcribe_audio(audio_path):

    if not GNANI_API_KEY:
        raise ValueError("Gnani API key not found.")

    headers = {
        "X-API-Key-ID": GNANI_API_KEY
    }

    data = {
        "language_code": "hi-IN",
        "preferred_language": "hi-IN",
        "format": "transcribe",
        "itn_native_numerals": "true"
    }

    with open(audio_path, "rb") as audio_file:

        files = {
            "audio_file": audio_file
        }

        response = requests.post(
            STT_URL,
            headers=headers,
            data=data,
            files=files,
            timeout=60
        )

    response.raise_for_status()

    result = response.json()

    return result.get("transcript", "")
