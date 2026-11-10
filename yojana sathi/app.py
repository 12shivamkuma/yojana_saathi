import os

import streamlit as st

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
    initial_sidebar_state="collapsed",
)


# ==================================================
# 2. HELPER: RENDER HTML CORRECTLY
# ==================================================
# WHY YOUR HTML WAS SHOWING AS TEXT:
# Streamlit's st.markdown() follows Markdown rules. Any line indented by
# 4 or more spaces is treated as a *code block*, and blank lines inside HTML
# can also break the block. Your HTML/CSS strings were indented, so they
# were printed as code instead of being rendered.
# This helper removes the indentation and blank lines before rendering.

def render_html(html: str) -> None:
    cleaned = "\n".join(
        line.strip() for line in html.splitlines() if line.strip()
    )
    st.markdown(cleaned, unsafe_allow_html=True)


# ==================================================
# 3. CUSTOM CSS
# ==================================================

render_html(
    """
    <style>

    /* Main background */
    .stApp {
        background: linear-gradient(180deg, #fffaf2 0%, #ffffff 50%, #f4faf5 100%);
    }

    /* Main container */
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Hero header */
    .hero {
        background: linear-gradient(120deg, #fff0dc, #ffffff, #eaf6ec);
        border: 1px solid #f0e5d6;
        border-radius: 22px;
        padding: 35px 25px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.04);
        margin-bottom: 22px;
    }
    .hero-icon {font-size: 48px; margin-bottom: 10px;}
    .hero-title {
        color: #173d2b;
        font-size: 40px;
        font-weight: 800;
        margin: 0;
        padding: 0;
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
            #ff9933 0%, #ff9933 33.33%,
            #ffffff 33.33%, #ffffff 66.66%,
            #138808 66.66%, #138808 100%
        );
        margin: 20px 0 28px 0;
        border: 1px solid #eeeeee;
    }

    /* Section headings */
    .section-heading {
        color: #173d2b;
        font-size: 23px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .section-description {
        color: #748078;
        font-size: 14px;
        margin-bottom: 18px;
    }

    /* Bordered cards (st.container(border=True)) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border-radius: 17px;
        box-shadow: 0 4px 16px rgba(20,60,35,0.05);
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
        box-shadow: 0 5px 14px rgba(221,112,27,0.25);
    }
    .stButton > button:active {
        transform: translateY(0);
    }

    /* Audio input and alerts */
    div[data-testid="stAudioInput"] {border-radius: 12px;}
    div[data-testid="stAlert"] {border-radius: 12px;}

    /* How-it-works step cards */
    .step-card {
        border-radius: 15px;
        padding: 19px 10px;
        text-align: center;
        min-height: 135px;
        transition: transform 0.2s ease;
    }
    .step-card:hover {transform: translateY(-3px);}
    .step-icon {font-size: 30px; margin-bottom: 8px;}
    .step-title {font-weight: 700; font-size: 15px;}
    .step-description {font-size: 12px; margin-top: 7px; color: #68736c;}

    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 22px 12px 5px 12px;
        color: #738078;
        font-size: 13px;
        line-height: 1.8;
    }
    .footer-brand {color: #254c35; font-size: 19px; font-weight: 800;}

    </style>
    """
)


# ==================================================
# 4. HERO SECTION
# ==================================================

render_html(
    """
    <div class="hero">
        <div class="hero-icon">🇮🇳</div>
        <h1 class="hero-title">Yojana Saathi</h1>
        <div class="hero-subtitle">आपकी सरकारी योजनाओं का साथी</div>
        <div class="hero-description">
            सरकारी योजनाओं की जानकारी अब आपकी अपनी भाषा में।
            <br>
            बस अपनी समस्या बोलिए और जानिए आपके लिए
            कौन-सी योजना उपयोगी हो सकती है।
        </div>
    </div>
    <div class="tricolour"></div>
    """
)


# ==================================================
# 5. VOICE INPUT SECTION
# ==================================================

render_html(
    """
    <div class="section-heading">🎙️ अपनी समस्या बताएं</div>
    <div class="section-description">
        हिंदी या Hinglish में अपनी समस्या रिकॉर्ड करें।
        Yojana Saathi आपकी बात समझने में मदद करेगा।
    </div>
    """
)

os.makedirs("audio", exist_ok=True)

with st.container(border=True):

    st.markdown("### 🎧 Voice Assistant")

    audio_input = st.audio_input("अपनी आवाज़ रिकॉर्ड करें")

    st.caption("उदाहरण: मुझे खेती के लिए सरकारी सहायता चाहिए।")

    process_button = st.button(
        "🔍 जानकारी प्राप्त करें",
        use_container_width=True,
    )


# ==================================================
# 6. AUDIO PROCESSING AND RESPONSE
# ==================================================
# Note: st.stop() was replaced with if/else so the "How it works" section
# and footer still appear even when the voice is not understood.

if process_button and audio_input is None:

    st.warning("कृपया पहले अपनी आवाज़ रिकॉर्ड करें।")

elif process_button and audio_input is not None:

    try:

        # Save recorded audio
        with open("audio/input.wav", "wb") as f:
            f.write(audio_input.getvalue())

        # Speech to Text
        with st.spinner("🎧 आपकी आवाज़ समझी जा रही है..."):
            query = transcribe_audio("audio/input.wav")

        if not query:

            st.error("आपकी आवाज़ समझ नहीं आई। कृपया दोबारा प्रयास करें।")

        else:

            st.success("आपकी बात सफलतापूर्वक समझ ली गई! ✓")

            # Display transcript
            st.markdown("### 💬 आपने क्या कहा?")

            with st.container(border=True):
                st.markdown("**आपका संदेश:**")
                st.write(query)

            # Find relevant schemes
            with st.spinner("📚 आपके लिए संबंधित सरकारी योजना खोजी जा रही है..."):
                schemes = find_schemes(query)

            # Generate answer
            with st.spinner("✍️ आपके लिए जवाब तैयार किया जा रहा है..."):
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

                st.write("आपके सवाल का जवाब आवाज़ में तैयार है।")

                with open(audio_path, "rb") as f:
                    st.audio(f.read(), format="audio/wav")

            st.success("धन्यवाद! Yojana Saathi का उपयोग करने के लिए। 🙏")

    except Exception as e:

        st.error(f"कुछ समस्या हुई: {e}")


# ==================================================
# 7. HOW IT WORKS
# ==================================================

st.markdown("---")

render_html(
    """
    <div class="section-heading">✨ Yojana Saathi कैसे काम करता है?</div>
    <div class="section-description">
        सिर्फ तीन आसान चरणों में सरकारी योजनाओं की जानकारी।
    </div>
    """
)

col1, col2, col3 = st.columns(3)

with col1:
    render_html(
        """
        <div class="step-card" style="background:#fff1e2;">
            <div class="step-icon">🎙️</div>
            <div class="step-title" style="color:#a95513;">अपनी बात कहें</div>
            <div class="step-description">हिंदी में सवाल पूछें।</div>
        </div>
        """
    )

with col2:
    render_html(
        """
        <div class="step-card" style="background:#edf4ff;">
            <div class="step-icon">📚</div>
            <div class="step-title" style="color:#285c91;">योजना खोजें</div>
            <div class="step-description">संबंधित योजना की जानकारी पाएं।</div>
        </div>
        """
    )

with col3:
    render_html(
        """
        <div class="step-card" style="background:#eaf7ed;">
            <div class="step-icon">🔊</div>
            <div class="step-title" style="color:#24723b;">जवाब सुनें</div>
            <div class="step-description">अपनी भाषा में जवाब सुनें।</div>
        </div>
        """
    )


# ==================================================
# 8. FOOTER
# ==================================================

render_html(
    """
    <div class="tricolour"></div>
    <div class="custom-footer">
        <div style="font-size:25px;">🇮🇳</div>
        <div class="footer-brand">Yojana Saathi</div>
        <p>सरकारी योजनाओं की जानकारी, अब आपकी भाषा में।</p>
        <p>
            यह ऐप प्रारंभिक जानकारी प्रदान करता है।
            पात्रता, आवेदन प्रक्रिया और लाभ की पुष्टि
            संबंधित आधिकारिक सरकारी स्रोतों से अवश्य करें।
        </p>
        <p style="margin-top:15px;">Made with ❤️ for India</p>
    </div>
    """
)
