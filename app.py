import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- AYARLAR ---
load_dotenv()
st.set_page_config(page_title="MONOLITH /// GEMINI", page_icon="💠", layout="wide", initial_sidebar_state="collapsed")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key: st.error("API Key eksik!"); st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- CSS TASARIMI (MONOLITH THEME) ---
st.markdown("""
<style>
    /* 1. FONT VE GENEL AYARLAR */
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

    /* 2. GİZLİLİK */
    #MainMenu, footer, header {visibility: hidden !important;}
    [data-testid="stSidebar"] { display: none !important; }
    .stDeployButton {display:none;}

    /* 3. HERO SECTION */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 8vh;
        margin-bottom: 60px;
        animation: fadeUp 1s ease-out;
    }
    
    .monolith-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 6rem; /* Yazı boyutu mobilde taşmasın diye biraz küçültüldü */
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

    /* 4. KARTLAR */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 25px;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    .obsidian-card {
        background: var(--card-dark);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 30px;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        cursor: pointer;
    }
    
    .obsidian-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 50px -10px rgba(0,0,0,0.5);
        border-color: rgba(var(--primary-glow), 0.5);
    }
    
    .card-icon {
        font-size: 2rem;
        margin-bottom: 20px;
        background: linear-gradient(135deg, rgba(var(--primary-glow), 1), rgba(var(--secondary-glow), 1));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .obsidian-card h3 {
        font-family: 'Space Grotesk', sans-serif;
        color: #fff;
        font-size: 1.25rem;
        margin: 0 0 10px 0;
    }
    
    .obsidian-card p {
        color: #888;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* 5. INPUT ALANI */
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

    /* 6. MESAJLAR */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        padding-bottom: 100px;
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

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# --- ANA MANTIK ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# HERO SECTION (Sadece mesaj yoksa görünür)
if not st.session_state.messages:
    st.markdown("""
    <div class="hero-container">
        <div class="monolith-title">MONOLITH</div>
        <div class="monolith-subtitle">SYSTEM v2.5 / FLASH ARCHITECTURE ONLINE</div>
    </div>
    
    <div class="grid-container" style="animation: fadeUp 1s ease-out 0.2s backwards;">
        <div class="obsidian-card">
            <div class="card-icon">⚡</div>
            <h3>Hyper-Speed Analysis</h3>
            <p>Execute complex data processing and algorithm optimization with near-instant latency.</p>
        </div>
        <div class="obsidian-card">
            <div class="card-icon">💠</div>
            <h3>Neural Architecture</h3>
            <p>Leverage next-gen Gemini models for deeply contextualized creative and logical tasks.</p>
        </div>
        <div class="obsidian-card">
            <div class="card-icon">🧬</div>
            <h3>Code Evolution</h3>
            <p>Debug, refactor, and generate production-ready code across multiple languages.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height: 150px;'></div>", unsafe_allow_html=True)

# SOHBET DÖNGÜSÜ
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'>{msg['content']}</div>", unsafe_allow_html=True)

# INPUT ALANI
if prompt := st.chat_input("Initiate command sequence..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

    try:
        history = [{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.messages]
        chat = model.start_chat(history=history[:-1])
        response = chat.send_message(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.markdown(f"<div class='bot-message'>{response.text}</div>", unsafe_allow_html=True)
        st.rerun()
        
    except Exception as e:
        st.error(f"System Error: {e}")
