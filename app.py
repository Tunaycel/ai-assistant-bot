import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# --- CONFIGURATION ---
load_dotenv()
st.set_page_config(page_title="MONOLITH /// VISION", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key: st.error("API Key missing! Please check .env file."); st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- MONOLITH THEME (CSS) ---
st.markdown("""
<style>
    /* 1. FONTS & BASICS */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    :root {
        --primary-glow: 0, 200, 255;
        --secondary-glow: 180, 50, 255;
        --bg-dark: #050507;
        --card-dark: #0a0a0f;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-dark);
        color: #e0e0e0;
    }

    .stApp {
        background: radial-gradient(circle at 50% 0%, rgba(var(--primary-glow), 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 80% 50%, rgba(var(--secondary-glow), 0.1) 0%, transparent 50%),
                    var(--bg-dark);
        background-attachment: fixed;
    }

    /* 2. HIDE STREAMLIT UI */
    #MainMenu, footer, header {visibility: hidden !important;}
    [data-testid="stSidebar"] { display: none !important; }
    .stDeployButton {display:none;}

    /* 3. HERO SECTION */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 5vh;
        margin-bottom: 30px;
        animation: fadeUp 1s ease-out;
    }
    
    .monolith-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 5rem;
        font-weight: 700;
        line-height: 1;
        letter-spacing: -0.03em;
        background: linear-gradient(to right, #fff 20%, rgba(var(--primary-glow), 1) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 80px rgba(var(--primary-glow), 0.3);
        margin-bottom: 15px;
        text-align: center;
    }
    
    .monolith-subtitle {
        font-family: 'Space Grotesk', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-size: 0.9rem;
        color: rgba(var(--primary-glow), 0.8);
        border: 1px solid rgba(var(--primary-glow), 0.3);
        padding: 8px 24px;
        border-radius: 4px;
        background: rgba(var(--primary-glow), 0.05);
        box-shadow: 0 0 30px rgba(var(--primary-glow), 0.1);
    }

    /* 4. INPUT FIELD */
    .stTextInput {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 900px;
        z-index: 1000;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(10, 10, 15, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 20px 25px !important;
        font-size: 1.1rem !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.6) !important;
        backdrop-filter: blur(20px);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(var(--primary-glow), 0.5) !important;
        background-color: rgba(10, 10, 15, 0.98) !important;
    }

    /* 5. CHAT BUBBLES */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        padding-bottom: 120px;
    }
    
    .user-message {
        background: rgba(var(--primary-glow), 0.1);
        border: 1px solid rgba(var(--primary-glow), 0.2);
        color: #fff;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0 10px auto;
        max-width: 80%;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .bot-message {
        background: var(--card-dark);
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: #d0d0d0;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px auto 10px 0;
        max-width: 80%;
    }

    /* 6. IMAGE STYLE */
    .uploaded-image {
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 10px;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- MAIN LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# HERO SECTION (Only visible when empty)
if not st.session_state.messages:
    st.markdown("""
    <div class="hero-container">
        <div class="monolith-title">MONOLITH</div>
        <div class="monolith-subtitle">SYSTEM v2.5 / VISION MODULE ONLINE</div>
    </div>
    """, unsafe_allow_html=True)

# VISUAL INPUT AREA
st.markdown("### 📸 Visual Input")
uploaded_file = st.file_uploader("Upload an image for analysis...", type=["jpg", "jpeg", "png"])

image_input = None
if uploaded_file:
    image_input = Image.open(uploaded_file)
    st.image(image_input, caption="Image Ready for Analysis", width=300)

# CHAT HISTORY
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'>{msg['content']}</div>", unsafe_allow_html=True)

# INPUT HANDLER
if prompt := st.chat_input("Initiate command sequence or analyze image..."):
    # Append User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

    try:
        # Generate Response (Text + Image OR Text Only)
        if image_input:
            response = model.generate_content([prompt, image_input])
        else:
            history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.messages if isinstance(m["content"], str)]
            chat = model.start_chat(history=history[:-1])
            response = chat.send_message(prompt)
        
        # Append Bot Response
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.markdown(f"<div class='bot-message'>{response.text}</div>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"System Error: {e}")