import math
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
# 2. HELPERS
# ==================================================

def render_html(html: str) -> None:
    """Render HTML safely: strips indentation/blank lines so Markdown
    does not turn the HTML into a code block."""
    cleaned = "\n".join(
        line.strip() for line in html.splitlines() if line.strip()
    )
    st.markdown(cleaned, unsafe_allow_html=True)


def chakra_svg(size: int = 64, color: str = "#1a237e") -> str:
    """Ashoka Chakra drawn as SVG (works on every device, unlike the
    flag emoji which shows as 'IN' on Windows)."""
    spokes = ""
    for i in range(24):
        a = math.radians(i * 15)
        x2 = 50 + 38 * math.cos(a)
        y2 = 50 + 38 * math.sin(a)
        spokes += (
            f'<line x1="50" y1="50" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="2"/>'
        )
    return (
        f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" '
        f'xmlns="http://www.w3.org/2000/svg">'
        f'<circle cx="50" cy="50" r="42" fill="none" stroke="{color}" stroke-width="5"/>'
        f'<circle cx="50" cy="50" r="6" fill="{color}"/>'
        f'{spokes}</svg>'
    )


# ==================================================
# 3. CUSTOM CSS  (colors are forced so text is always visible,
#    even if the browser or Streamlit is in dark mode)
# ==================================================

render_html(
    """
    <style>

    /* ---------- Base: force light look ---------- */
    :root, .stApp, [data-testid="stAppViewContainer"] {
        color-scheme: light;
    }
    .stApp {
        background:
            radial-gradient(circle at 0% 0%, #ffe7c7 0%, transparent 40%),
            radial-gradient(circle at 100% 100%, #d9f2e0 0%, transparent 40%),
            #fffaf2;
    }
    header[data-testid="stHeader"] {background: transparent;}
    #MainMenu, footer {visibility: hidden;}

    .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* ---------- Force readable text everywhere ---------- */
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stWidgetLabel"] p,
    label p {
        color: #1f3d2b !important;
    }
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] * {
        color: #55665b !important;
    }
    [data-testid="stSpinner"] * {color: #1f3d2b !important;}

    /* ---------- Hero ---------- */
    .hero {
        position: relative;
        background: linear-gradient(135deg, #0f4c3a 0%, #166a4d 55%, #1f8a5b 100%);
        border-radius: 26px;
        padding: 36px 24px 30px 24px;
        text-align: center;
        box-shadow: 0 14px 34px rgba(15,76,58,0.28);
        overflow: hidden;
    }
    .hero::before {
        content: "";
        position: absolute;
        top: -70px; right: -70px;
        width: 220px; height: 220px;
        border-radius: 50%;
        background: rgba(255,153,51,0.35);
    }
    .hero::after {
        content: "";
        position: absolute;
        bottom: -80px; left: -60px;
        width: 220px; height: 220px;
        border-radius: 50%;
        background: rgba(255,255,255,0.10);
    }
    .hero > * {position: relative; z-index: 1;}
    .hero-badge {
        width: 84px; height: 84px;
        margin: 0 auto 14px auto;
        background: #ffffff;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        border: 4px solid #ff9933;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    }
    .hero-title {
        color: #ffffff !important;
        font-size: 46px;
        font-weight: 800;
        letter-spacing: -1px;
        line-height: 1.1;
        margin: 0;
    }
    .hero-subtitle {
        color: #ffc46b !important;
        font-size: 22px;
        font-weight: 700;
        margin-top: 10px;
    }
    .hero-description {
        color: #f1fff6 !important;
        font-size: 16px;
        line-height: 1.8;
        margin-top: 12px;
    }
    .chip-row {
        display: flex; flex-wrap: wrap;
        justify-content: center; gap: 10px;
        margin-top: 20px;
    }
    .chip {
        background: #ffffff;
        color: #0f4c3a !important;
        font-size: 13px;
        font-weight: 700;
        padding: 7px 14px;
        border-radius: 999px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    /* ---------- Tricolour line ---------- */
    .tricolour {
        height: 7px;
        border-radius: 10px;
        background: linear-gradient(
            to right,
            #ff9933 0%, #ff9933 33.33%,
            #ffffff 33.33%, #ffffff 66.66%,
            #138808 66.66%, #138808 100%
        );
        margin: 22px 0 28px 0;
        border: 1px solid #e3e3e3;
    }

    /* ---------- Section headings ---------- */
    .section-heading {
        color: #0f4c3a !important;
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .section-description {
        color: #55665b !important;
        font-size: 15px;
        margin-bottom: 16px;
    }

    /* ---------- Cards (st.container(border=True)) ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border: 2px solid #ffd9a8;
        border-radius: 20px;
        box-shadow: 0 8px 22px rgba(232,121,36,0.12);
    }

    /* ---------- Example prompt chips ---------- */
    .example-label {
        color: #55665b !important;
        font-size: 13px;
        font-weight: 600;
        margin: 6px 0 8px 0;
    }
    .example-chip {
        display: inline-block;
        background: #fff1de;
        color: #9a4a0c !important;
        border: 1px solid #ffd2a0;
        font-size: 13px;
        font-weight: 600;
        padding: 6px 12px;
        border-radius: 999px;
        margin: 0 6px 8px 0;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        background: linear-gradient(90deg, #ff7a18, #ff9f1c);
        border: none;
        border-radius: 14px;
        min-height: 54px;
        width: 100%;
        box-shadow: 0 6px 16px rgba(255,122,24,0.35);
        transition: all 0.2s ease;
    }
    .stButton > button p {
        color: #ffffff !important;
        font-size: 18px;
        font-weight: 800;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #f06a0a, #ff9000);
        border: none;
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(255,122,24,0.45);
    }
    .stButton > button:active {transform: translateY(0);}

    /* ---------- Audio input and alerts ---------- */
    div[data-testid="stAudioInput"] {border-radius: 14px;}
    div[data-testid="stAlert"] {
        border-radius: 14px;
        background: #ffffff;
        border: 1.5px solid #cfe3d6;
    }
    div[data-testid="stAlert"] * {color: #1f3d2b !important;}

    /* ---------- Steps ---------- */
    .step-card {
        border-radius: 20px;
        padding: 24px 12px;
        text-align: center;
        min-height: 160px;
        color: #ffffff;
        box-shadow: 0 8px 20px rgba(0,0,0,0.14);
        transition: transform 0.2s ease;
    }
    .step-card:hover {transform: translateY(-4px);}
    .step-num {
        display: inline-block;
        width: 26px; height: 26px; line-height: 26px;
        border-radius: 50%;
        background: rgba(255,255,255,0.95);
        font-size: 13px; font-weight: 800;
        margin-bottom: 6px;
    }
    .step-icon {font-size: 34px; margin-bottom: 6px;}
    .step-title {font-weight: 800; font-size: 17px; color: #ffffff !important;}
    .step-description {
        font-size: 13px; margin-top: 6px;
        color: #ffffff !important;
        opacity: 0.95;
    }

    /* ---------- Footer ---------- */
    .custom-footer {
        text-align: center;
        padding: 10px 12px 4px 12px;
        font-size: 13px;
        line-height: 1.8;
    }
    .custom-footer p {color: #55665b !important; margin: 6px 0;}
    .footer-brand {color: #0f4c3a !important; font-size: 21px; font-weight: 800;}

    </style>
    """
)


# ==================================================
# 4. HERO SECTION
# ==================================================

render_html(
    f"""
    <div class="hero">
        <div class="hero-badge">{chakra_svg(58)}</div>
        <div class="hero-title">Yojana Saathi</div>
        <div class="hero-subtitle">आपकी सरकारी योजनाओं का साथी</div>
        <div class="hero-description">
            सरकारी योजनाओं की जानकारी अब आपकी अपनी भाषा में।
            <br>
            बस अपनी समस्या बोलिए और जानिए आपके लिए
            कौन-सी योजना उपयोगी हो सकती है।
        </div>
        <div class="chip-row">
            <span class="chip">🗣️ हिंदी और Hinglish</span>
            <span class="chip">🔊 आवाज़ में जवाब</span>
            <span class="chip">🆓 पूरी तरह मुफ़्त</span>
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

    render_html(
        """
        <div class="example-label">💡 आप ऐसे बोल सकते हैं:</div>
        <span class="example-chip">🌾 खेती के लिए सरकारी सहायता चाहिए</span>
        <span class="example-chip">🎓 पढ़ाई के लिए छात्रवृत्ति</span>
        <span class="example-chip">🏠 घर बनाने के लिए योजना</span>
        <span class="example-chip">🏥 इलाज के लिए मदद</span>
        <span class="example-chip">👩 महिलाओं के लिए योजना</span>
        """
    )

    process_button = st.button(
        "🔍 जानकारी प्राप्त करें",
        use_container_width=True,
    )


# ==================================================
# 6. AUDIO PROCESSING AND RESPONSE
# ==================================================

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

render_html('<div class="tricolour"></div>')

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
        <div class="step-card" style="background:linear-gradient(135deg,#ff7a18,#ffa63d);">
            <div class="step-num" style="color:#c2570c;">1</div>
            <div class="step-icon">🎙️</div>
            <div class="step-title">अपनी बात कहें</div>
            <div class="step-description">हिंदी में सवाल पूछें।</div>
        </div>
        """
    )

with col2:
    render_html(
        """
        <div class="step-card" style="background:linear-gradient(135deg,#2563eb,#4f9bff);">
            <div class="step-num" style="color:#1d4ed8;">2</div>
            <div class="step-icon">📚</div>
            <div class="step-title">योजना खोजें</div>
            <div class="step-description">संबंधित योजना की जानकारी पाएं।</div>
        </div>
        """
    )

with col3:
    render_html(
        """
        <div class="step-card" style="background:linear-gradient(135deg,#0f8a3c,#35b565);">
            <div class="step-num" style="color:#0b6b2e;">3</div>
            <div class="step-icon">🔊</div>
            <div class="step-title">जवाब सुनें</div>
            <div class="step-description">अपनी भाषा में जवाब सुनें।</div>
        </div>
        """
    )


# ==================================================
# 8. FOOTER
# ==================================================

render_html(
    f"""
    <div class="tricolour" style="margin-top:34px;"></div>
    <div class="custom-footer">
        <div>{chakra_svg(40)}</div>
        <div class="footer-brand">Yojana Saathi</div>
        <p>सरकारी योजनाओं की जानकारी, अब आपकी भाषा में।</p>
        <p>
            यह ऐप प्रारंभिक जानकारी प्रदान करता है।
            पात्रता, आवेदन प्रक्रिया और लाभ की पुष्टि
            संबंधित आधिकारिक सरकारी स्रोतों से अवश्य करें।
        </p>
        <p style="margin-top:14px;">Made with ❤️ for India</p>
    </div>
    """
)
