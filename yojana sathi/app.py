
import streamlit as st
import os

from utils.stt import transcribe_audio
from utils.retriever import find_schemes
from utils.response import generate_response
from utils.tts import generate_speech


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Yojana Saathi",
    page_icon="🇮🇳",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ==================================================
# 2. CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            180deg,
            #fffaf2 0%,
            #ffffff 50%,
            #f4faf5 100%
        );
    }

    /* Main container */
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

    /* Header */
    .hero {
        background: linear-gradient(
            120deg,
            #fff0dc,
            #ffffff,
            #eaf6ec
        );
        border: 1px solid #f0e5d6;
        border-radius: 22px;
        padding: 35px 25px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.04);
        margin-bottom: 22px;
    }

    .hero-icon {
        font-size: 48px;
        margin-bottom: 10px;
    }

    .hero-title {
        color: #173d2b;
        font-size: 40px;
        font-weight: 800;
        margin: 0;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        color: #b65d17;
        font-size: 20px;
        font-weight: 700;
        margin-top: 10px;
    }

    .hero-description {
        color: #58665e;
        font-size: 15px;
        line-height: 1.8;
        margin-top: 13px;
    }

    /* Tricolour line */
    .tricolour {
        height: 5px;
        border-radius: 10px;
        background: linear-gradient(
            to right,
            #ff9933 0%,
            #ff9933 33.33%,
            #ffffff 33.33%,
            #ffffff 66.66%,
            #138808 66.66%,
            #138808 100%
        );
        margin: 20px 0 28px 0;
        border: 1px solid #eeeeee;
    }

    /* Section heading */
    .section-heading {
        color: #173d2b;
        font-size: 23px;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .section-description {
        color: #748078;
        font-size: 14px;
        margin-bottom: 18px;
    }

    /* Cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border: 1px solid #e6eee8;
        border-radius: 17px;
        box-shadow: 0 4px 16px rgba(20,60,35,0.04);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(
            90deg,
            #e87924,
            #f39b36
        );
        color: white;
        border: none;
        border-radius: 12px;
        min-height: 48px;
        font-size: 16px;
        font-weight: 700;
        width: 100%;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(
            90deg,
            #d96816,
            #e98524
        );
        color: white;
        border: none;
        transform: translateY(-1px);
        box-shadow: 0 5px 14px rgba(221,112,27,0.2);
    }

    /* Audio input */
    div[data-testid="stAudioInput"] {
        border-radius: 12px;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 22px 12px 5px 12px;
        color: #738078;
        font-size: 13px;
        line-height: 1.8;
    }

    .footer-brand {
        color: #254c35;
        font-size: 19px;
        font-weight: 800;
    }

    /* Process cards */
    .step-card {
        border-radius: 15px;
        padding: 19px 10px;
        text-align: center;
        min-height: 135px;
    }

    .step-icon {
        font-size: 30px;
        margin-bottom: 8px;
    }

    .step-title {
        font-weight: 750;
        font-size: 15px;
    }

    .step-description {
        font-size: 12px;
        margin-top: 7px;
        color: #68736c;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 3. HERO SECTION
# ==================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-icon">🇮🇳</div>

        <h1 class="hero-title">Yojana Saathi</h1>

        <div class="hero-subtitle">
            आपकी सरकारी योजनाओं का साथी
        </div>

        <div class="hero-description">
            सरकारी योजनाओं की जानकारी अब आपकी अपनी भाषा में।
            <br>
            बस अपनी समस्या बोलिए और जानिए आपके लिए
            कौन-सी योजना उपयोगी हो सकती है।
        </div>

    </div>

    <div class="tricolour"></div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 4. VOICE INPUT SECTION
# ==================================================

st.markdown(
    """
    <div class="section-heading">
        🎙️ अपनी समस्या बताएं
    </div>

    <div class="section-description">
        हिंदी या Hinglish में अपनी समस्या रिकॉर्ड करें।
        Yojana Saathi आपकी बात समझने में मदद करेगा।
    </div>
    """,
    unsafe_allow_html=True
)


os.makedirs("audio", exist_ok=True)

with st.container(border=True):

    st.markdown("### 🎧 Voice Assistant")

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


# ==================================================
# 5. AUDIO PROCESSING AND RESPONSE
# ==================================================

if audio_input is not None and process_button:

    try:

        # Save recorded audio
        with open("audio/input.wav", "wb") as f:
            f.write(audio_input.getvalue())

        # Speech to Text
        with st.spinner("🎧 आपकी आवाज़ समझी जा रही है..."):

            query = transcribe_audio("audio/input.wav")

        if not query:

            st.error(
                "आपकी आवाज़ समझ नहीं आई। कृपया दोबारा प्रयास करें।"
            )

            st.stop()

        st.success("आपकी बात सफलतापूर्वक समझ ली गई! ✓")


        # Display transcript
        st.markdown("### 💬 आपने क्या कहा?")

        with st.container(border=True):

            st.markdown("**आपका संदेश:**")

            st.write(query)


        # Find relevant schemes
        with st.spinner(
            "📚 आपके लिए संबंधित सरकारी योजना खोजी जा रही है..."
        ):

            schemes = find_schemes(query)


        # Generate answer
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

            st.write(
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


# ==================================================
# 6. HOW IT WORKS
# ==================================================

st.markdown("---")

st.markdown(
    """
    <div class="section-heading">
        ✨ Yojana Saathi कैसे काम करता है?
    </div>

    <div class="section-description">
        सिर्फ तीन आसान चरणों में सरकारी योजनाओं की जानकारी।
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
        <div class="step-card" style="background:#fff1e2;">

            <div class="step-icon">🎙️</div>

            <div class="step-title" style="color:#a95513;">
                अपनी बात कहें
            </div>

            <div class="step-description">
                हिंदी में सवाल पूछें।
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="step-card" style="background:#edf4ff;">

            <div class="step-icon">📚</div>

            <div class="step-title" style="color:#285c91;">
                योजना खोजें
            </div>

            <div class="step-description">
                संबंधित योजना की जानकारी पाएं।
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="step-card" style="background:#eaf7ed;">

            <div class="step-icon">🔊</div>

            <div class="step-title" style="color:#24723b;">
                जवाब सुनें
            </div>

            <div class="step-description">
                अपनी भाषा में जवाब सुनें।
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# 7. FOOTER
# ==================================================

st.markdown(
    """
    <div class="tricolour"></div>

    <div class="custom-footer">

        <div style="font-size:25px;">🇮🇳</div>

        <div class="footer-brand">
            Yojana Saathi
        </div>

        <p>
            सरकारी योजनाओं की जानकारी, अब आपकी भाषा में।
        </p>

        <p>
            यह ऐप प्रारंभिक जानकारी प्रदान करता है।
            पात्रता, आवेदन प्रक्रिया और लाभ की पुष्टि
            संबंधित आधिकारिक सरकारी स्रोतों से अवश्य करें।
        </p>

        <p style="margin-top:15px;">
            Made with ❤️ for India
        </p>

    </div>
    """,
    unsafe_allow_html=True
)
