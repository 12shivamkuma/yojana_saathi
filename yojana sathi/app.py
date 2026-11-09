
import streamlit as st
import os

from utils.stt import transcribe_audio
from utils.retriever import find_schemes
from utils.response import generate_response
from utils.tts import generate_speech

st.set_page_config(
    page_title="Yojana Saathi",
    page_icon="🇮🇳",
    layout="centered"
)

st.title("🇮🇳 Yojana Saathi")
st.subheader("आपकी सरकारी योजनाओं का साथी")

st.write(
    "अपनी समस्या हिंदी में बताएं। "
    "मैं आपके लिए संबंधित सरकारी योजना खोजने में मदद करूंगा।"
)

os.makedirs("audio", exist_ok=True)

audio_input = st.audio_input("अपनी आवाज़ रिकॉर्ड करें")

if audio_input is not None:
    if st.button("जानकारी प्राप्त करें"):

        with st.spinner("आपकी आवाज़ समझी जा रही है..."):

            with open("audio/input.wav", "wb") as f:
                f.write(audio_input.getvalue())

            try:
                query = transcribe_audio("audio/input.wav")

                if not query:
                    st.error("आपकी आवाज़ समझ नहीं आई। दोबारा प्रयास करें।")
                    st.stop()

                st.success("आपकी बात समझ ली गई!")
                st.write("**आपने कहा:**", query)

                schemes = find_schemes(query)

                answer = generate_response(query, schemes)

                st.subheader("आपके लिए जानकारी")
                st.write(answer)

                with st.spinner("आवाज़ तैयार की जा रही है..."):

                    audio_path = generate_speech(answer)

                st.subheader("🔊 जवाब सुनें")

                with open(audio_path, "rb") as f:
                    st.audio(f.read(), format="audio/wav")

            except Exception as e:
                st.error(f"कुछ समस्या हुई: {e}")

st.divider()
st.caption(
    "Yojana Saathi provides preliminary information. "
    "Always verify eligibility through official government sources."
)
