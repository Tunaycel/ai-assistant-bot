import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import PyPDF2

# --- CONFIGURATION ---
load_dotenv()
st.set_page_config(page_title="Monolith AI", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

# --- API SETUP ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key: st.error("API Key missing! Check .env file."); st.stop()

genai.configure(api_key=api_key)
# EN YENI MODEL (Flash)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# --- ULTIMATE DESIGN (GLASSMORPHISM) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&family=Plus+Jakarta+Sans:wght@400;600&display=swap');
    
    :root {
        --primary: #6366f1;
        --secondary: #a855f7;
        --bg-dark: #09090b;
        --glass: rgba(255, 255, 255, 0.03);
        --border: rgba(255, 255, 255, 0.08);
    }

    /* Main Background with Animated Gradient */
    .stApp {
        background-color: var(--bg-dark);
        background-image: 
            radial-gradient(circle at 0% 0%, rgba(99, 102, 241, 0.15), transparent 40%),
            radial-gradient(circle at 100% 100%, rgba(168, 85, 247, 0.15), transparent 40%);
        background-attachment: fixed;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* HIDE DEFAULTS */
    #MainMenu, footer, header {visibility: hidden !important;}
    .stDeployButton {display:none;}

    /* SIDEBAR (GLASS) */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 15, 20, 0.8);
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--border);
    }
    
    section[data-testid="stSidebar"] h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
        letter-spacing: 1px;
        color: #e2e8f0;
    }

    /* BRANDING */
    .brand-container {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid var(--border);
    }
    .brand-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
    }
    .brand-badge {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: white;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
    }

    /* CARDS & UPLOADERS */
    [data-testid="stFileUploader"] {
        background: var(--glass);
        border: 1px dashed var(--border);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary);
        background: rgba(99, 102, 241, 0.05);
        transform: translateY(-2px);
    }

    /* CHAT MESSAGES */
    .user-msg {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(79, 70, 229, 0.1));
        border: 1px solid rgba(99, 102, 241, 0.2);
        color: #e0e7ff;
        padding: 18px 24px;
        border-radius: 20px 20px 4px 20px;
        margin: 10px 0 10px auto;
        max-width: 80%;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        font-size: 0.95rem;
    }
    
    .bot-msg {
        background: var(--glass);
        border: 1px solid var(--border);
        color: #cbd5e1;
        padding: 18px 24px;
        border-radius: 20px 20px 20px 4px;
        margin: 10px auto 10px 0;
        max-width: 80%;
        font-size: 0.95rem;
    }

    /* INPUT FIELD (FLOATING) */
    .stTextInput {
        position: fixed;
        bottom: 40px;
        left: 50%;
        transform: translateX(-50%);
        width: 85%;
        max-width: 800px;
        z-index: 1000;
    }
    .stTextInput input {
        background: rgba(20, 20, 25, 0.8) !important;
        backdrop-filter: blur(15px);
        border: 1px solid var(--border) !important;
        color: white !important;
        border-radius: 100px !important;
        padding: 25px 35px !important;
        font-size: 1rem !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }
    .stTextInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.3);
    }

    /* Spacer for chat */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        padding-bottom: 140px;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC FUNCTIONS ---
def get_pdf_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return "".join(p.extract_text() for p in reader.pages)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div class="brand-container">
            <div class="brand-title">Monolith</div>
            <span class="brand-badge">Ultimate AI</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📂 Intelligence Hub")
    
    with st.expander("📄 Document Analysis", expanded=True):
        pdf_file = st.file_uploader("Upload PDF", type=['pdf'], label_visibility="collapsed")
        pdf_text = ""
        if pdf_file:
            with st.spinner("Processing neural data..."):
                pdf_text = get_pdf_text(pdf_file)
            st.success("Document Indexed")

    with st.expander("👁️ Vision Core", expanded=True):
        img_file = st.file_uploader("Upload Image", type=['png','jpg','jpeg'], label_visibility="collapsed")
        image_input = None
        if img_file:
            image_input = Image.open(img_file)
            st.image(image_input, use_column_width=True)
            st.success("Vision Active")
            
    st.markdown("---")
    if st.button("Reset System"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Intro (Only if empty)
if not st.session_state.messages:
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 60vh; text-align: center;">
        <h1 style="font-size: 4rem; background: linear-gradient(to right, #fff, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">MONOLITH AI</h1>
        <p style="color: #64748b; font-size: 1.2rem; max-width: 600px;">
            The ultimate convergence of Text, Vision, and Data analysis. <br>
            Upload a document or image to begin.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Chat History
for msg in st.session_state.messages:
    style = "user-msg" if msg["role"] == "user" else "bot-msg"
    st.markdown(f"<div class='{style}'>{msg['content']}</div>", unsafe_allow_html=True)

# Logic
if prompt := st.chat_input("Command the system..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='user-msg'>{prompt}</div>", unsafe_allow_html=True)

    try:
        response_text = ""
        if pdf_text:
            full_prompt = f"DOCUMENT CONTEXT:\n{pdf_text[:20000]}\n\nUSER QUESTION:\n{prompt}"
            if image_input:
                response = model.generate_content([full_prompt, image_input])
            else:
                response = model.generate_content(full_prompt)
        elif image_input:
            response = model.generate_content([prompt, image_input])
        else:
            chat = model.start_chat(history=[{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.messages if isinstance(m["content"], str)][:-1])
            response = chat.send_message(prompt)
            
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.markdown(f"<div class='bot-msg'>{response.text}</div>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"System Error: {e}")