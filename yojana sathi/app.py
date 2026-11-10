
import streamlit as st
import os

from utils.stt import transcribe_audio
from utils.retriever import find_schemes
from utils.response import generate_response
from utils.tts import generate_speech


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Yojana Saathi | सरकारी योजनाओं का साथी",
    page_icon="🇮🇳",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# CUSTOM CSS - INTERFACE ONLY
# --------------------------------------------------

st.markdown("""
<style>

/* Main application background */
.stApp {
    background: linear-gradient(
        180deg,
        #fffaf2 0%,
        #ffffff 45%,
        #f3faf5 100%
    );
}

/* Main content width and spacing */
.block-container {
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Hero section */
.hero {
    background: linear-gradient(
        120deg,
        #fff0d9,
        #ffffff 55%,
        #e9f7ed
    );
    border: 1px solid #f0e4d2;
    border-radius: 22px;
    padding: 35px 28px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 5px 22px rgba(0,0,0,0.04);
}

.hero-icon {
    font-size: 48px;
    margin-bottom: 8px;
}

.hero h1 {
    color: #173b2b;
    font-size: 38px;
    font-weight: 800;
    margin: 0;
    letter-spacing: -1px;
}

.hero-subtitle {
    color: #b45c13;
    font-size: 20px;
    font-weight: 700;
    margin-top: 10px;
}

.hero-description {
    color: #52645a;
    font-size: 15px;
    margin-top: 12px;
    line-height: 1.7;
}

/* Section headings */
.section-heading {
    color: #173b2b;
    font-size: 22px;
    font-weight: 750;
    margin-bottom: 6px;
}

.section-description {
    color: #718078;
    font-size: 14px;
    margin-bottom: 18px;
}

/* Information cards */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.92);
    border: 1px solid #e8eee9;
    border-radius: 17px;
    box-shadow: 0 4px 18px rgba(22,60,39,0.045);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #e87924, #f39b36);
    color: white;
    border: none;
    border-radius: 12px;
    min-height: 48px;
    font-size: 16px;
    font-weight: 700;
    width: 100%;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #d96816, #e98524);
    color: white;
    border: none;
    transform: translateY(-1px);
    box-shadow: 0 5px 14px rgba(221,112,27,0.2);
}

/* Audio input */
div[data-testid="stAudioInput"] {
    border-radius: 12px;
}

/* Success and error messages */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Footer */
.custom-footer {
    text-align: center;
    padding: 22px 12px 5px 12px;
    color: #738078;
    font-size: 12px;
    line-height: 1.8;
}

/* Tricolour divider */
.tricolour {
    height: 5px;
    border-radius: 10px;
    background: linear-gradient(
        90deg,
        #ff9933 0%,
        #ff9933 33.33%,
        #ffffff 33.33%,
        #ffffff 66.66%,
        #138808 66.66%,
        #138808 100%
    );
    margin: 18px 0 25px 0;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown("""
<div class="hero">

    <div class="hero-icon">🇮🇳</div>

    <h1>Yojana Saathi</h1>

    <div class="hero-subtitle">
        आपकी सरकारी योजनाओं का साथी
    </div>

    <div class="hero-description">
        सरकारी योजनाओं की जानकारी अब आपकी अपनी भाषा में।<br>
        बस अपनी समस्या बोलिए और जानिए आपके लिए कौन-सी योजना उपयोगी हो सकती है।
    </div>

</div>

<div class="tricolour"></div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# VOICE INPUT SECTION
# --------------------------------------------------

st.markdown("""
<div class="section-heading">
    🎙️ अपनी समस्या बताएं
</div>

<div class="section-description">
    नीचे दिए गए माइक्रोफोन से अपनी बात हिंदी या Hinglish में रिकॉर्ड करें।
</div>
""", unsafe_allow_html=True)


os.makedirs("audio", exist_ok=True)

with st.container(border=True):

    st.markdown("#### 🎧 Voice Assistant")

    audio_input = st.audio_input(
        "अपनी आवाज़ रिकॉर्ड करें"
    )

    st.caption(
        "उदाहरण: मुझे खेती के लिए सरकारी सहायता चाहिए।"
    )

    process_button = st.button(
        "🔍 जानकारी प्राप्त करें",
        use_container_width=True
    )


# --------------------------------------------------
# PROCESSING AND RESPONSE
# --------------------------------------------------

if audio_input is not None and process_button:

    with st.spinner("🎧 आपकी आवाज़ समझी जा रही है..."):

        with open("audio/input.wav", "wb") as f:
            f.write(audio_input.getvalue())

        try:

            # Speech to Text
            query = transcribe_audio("audio/input.wav")

            if not query:
                st.error(
                    "आपकी आवाज़ समझ नहीं आई। कृपया दोबारा प्रयास करें।"
                )
                st.stop()

            st.success("आपकी बात सफलतापूर्वक समझ ली गई!")

            # Display transcript
            st.markdown("### 💬 आपने क्या कहा?")

            with st.container(border=True):
                st.markdown(
                    f"**आपका संदेश:**  \n{query}"
                )

            # Find relevant schemes
            with st.spinner("📚 आपके लिए संबंधित सरकारी योजना खोजी जा रही है..."):

                schemes = find_schemes(query)

            # Generate response
            answer = generate_response(query, schemes)

            # Display answer
            st.markdown("### 🇮🇳 आपके लिए जानकारी")

            with st.container(border=True):

                st.markdown("#### 📋 योजना से जुड़ी जानकारी")

                st.markdown(answer)

            # Generate speech
            with st.spinner("🔊 आपके लिए आवाज़ तैयार की जा रही है..."):

                audio_path = generate_speech(answer)

            # Display generated audio
            st.markdown("### 🔊 जवाब सुनें")

            with st.container(border=True):

                st.markdown(
                    "आपके सवाल का जवाब आवाज़ में तैयार है।"
                )

                with open(audio_path, "rb") as f:
                    st.audio(
                        f.read(),
                        format="audio/wav"
                    )

            st.success(
                "धन्यवाद! Yojana Saathi का उपयोग करने के लिए। 🙏"
            )

        except Exception as e:

            st.error(f"कुछ समस्या हुई: {e}")


elif process_button and audio_input is None:

    st.warning(
        "कृपया पहले अपनी आवाज़ रिकॉर्ड करें।"
    )


# --------------------------------------------------
# HOW IT WORKS
# --------------------------------------------------

st.markdown("---")

st.markdown("""
<div class="section-heading">
    ✨ Yojana Saathi कैसे काम करता है?
</div>

<div class="section-description">
    आपकी आवाज़ से लेकर योजना की जानकारी तक, सब कुछ आसान तरीके से।
</div>
""", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="
        background:#fff2e4;
        border-radius:14px;
        padding:17px 10px;
        text-align:center;
        min-height:125px;
    ">
        <div style="font-size:29px;">🎙️</div>
        <b style="color:#a95513;">अपनी बात कहें</b>
        <p style="font-size:12px;color:#6c6c6c;">
            हिंदी में सवाल पूछें
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        background:#edf4ff;
        border-radius:14px;
        padding:17px 10px;
        text-align:center;
        min-height:125px;
    ">
        <div style="font-size:29px;">📚</div>
        <b style="color:#285c91;">योजना खोजें</b>
        <p style="font-size:12px;color:#6c6c6c;">
            संबंधित जानकारी प्राप्त करें
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
        background:#eaf7ed;
        border-radius:14px;
        padding:17px 10px;
        text-align:center;
        min-height:125px;
    ">
        <div style="font-size:29px;">🔊</div>
        <b style="color:#24723b;">जवाब सुनें</b>
        <p style="font-size:12px;color:#6c6c6c;">
            अपनी भाषा में जवाब पाएं
        </p>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="tricolour"></div>

<div class="custom-footer">

    <div style="font-size:22px;">🇮🇳</div>

    <b style="color:#254c35;font-size:15px;">
        Yojana Saathi
    </b>

    <p>
        सरकारी योजनाओं की जानकारी, अब आपकी भाषा में।
    </p>

    <p>
        यह ऐप प्रारंभिक जानकारी प्रदान करता है।<br>
        पात्रता, आवेदन प्रक्रिया और लाभ की पुष्टि
        संबंधित आधिकारिक सरकारी स्रोतों से अवश्य करें।
    </p>

    <p style="margin-top:15px;">
        Made with ❤️ for India
    </p>

</div>
""", unsafe_allow_html=True)
