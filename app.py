import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# --- AYARLAR ---
load_dotenv()
st.set_page_config(page_title="MONOLITH /// VISION", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key: st.error("API Key eksik!"); st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- CSS TASARIMI ---
st.markdown("""
<style>
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

    #MainMenu, footer, header {visibility: hidden !important;}
    [data-testid="stSidebar"] { display: none !important; }

    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 5vh;
        margin-bottom: 30px;
    }
    
    .monolith-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(to right, #fff 20%, rgba(var(--primary-glow), 1) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 50px rgba(var(--primary-glow), 0.3);
        text-align: center;
    }

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
    }

    .user-message {
        background: rgba(var(--primary-glow), 0.1);
        border: 1px solid rgba(var(--primary-glow), 0.2);
        color: #fff;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0 10px auto;
        max-width: 80%;
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
</style>
""", unsafe_allow_html=True)

# --- ANA MANTIK ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# BAŞLIK
if not st.session_state.messages:
    st.markdown("""
    <div class="hero-container">
        <div class="monolith-title">MONOLITH</div>
        <div style="color: #666; margin-top: 10px;">VISION MODULE ONLINE</div>
    </div>
    """, unsafe_allow_html=True)

# --- BU KISIM EKSİKTİ: RESİM YÜKLEME ALANI ---
st.markdown("### 📸 Görsel Yükle (Vision)")
uploaded_file = st.file_uploader("Analiz edilecek resmi seçin...", type=["jpg", "jpeg", "png"])

image_input = None
if uploaded_file:
    image_input = Image.open(uploaded_file)
    st.image(image_input, caption="Görsel Hazır", width=300)

# SOHBET GEÇMİŞİ
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'>{msg['content']}</div>", unsafe_allow_html=True)

# GİRDİ ALANI
if prompt := st.chat_input("Bir şeyler sor veya resmi yorumla..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

    try:
        # Eğer resim varsa modele hem metni hem resmi atıyoruz
        if image_input:
            response = model.generate_content([prompt, image_input])
        else:
            # Sadece metin varsa normal sohbet
            chat = model.start_chat()
            response = chat.send_message(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.markdown(f"<div class='bot-message'>{response.text}</div>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Hata: {e}")