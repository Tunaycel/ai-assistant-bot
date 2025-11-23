import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from PIL import Image

load_dotenv()

st.set_page_config(page_title="Monolith AI", page_icon="◆", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
    
    /* Modern Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 25%, #1e1b4b 50%, #1e293b 75%, #0f172a 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 80% 50%, rgba(168, 85, 247, 0.15) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .block-container { padding: 3rem 4rem !important; max-width: 1100px !important; }
    
    /* Premium Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(30, 27, 75, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(99, 102, 241, 0.2);
        box-shadow: 4px 0 30px rgba(0, 0, 0, 0.3);
    }
    
    section[data-testid="stSidebar"] > div { padding: 2rem 1.5rem; }
    
    section[data-testid="stSidebar"] h2 {
        color: #e0e7ff !important;
        font-size: 0.75rem !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin: 2rem 0 1.5rem !important;
        background: linear-gradient(135deg, #818cf8, #c4b5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #c7d2fe !important;
        font-size: 0.938rem !important;
        font-weight: 600 !important;
        margin: 2rem 0 1rem !important;
    }
    
    /* Premium File Upload */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.08) 100%);
        border: 2px solid rgba(129, 140, 248, 0.3);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="stFileUploader"]::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(129, 140, 248, 0.2), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    [data-testid="stFileUploader"]:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.12) 100%);
        border-color: rgba(129, 140, 248, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.2);
    }
    
    [data-testid="stFileUploader"] section { border: none !important; padding: 0 !important; }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.2s !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    }
    
    [data-testid="stFileUploader"] small { color: #a5b4fc !important; font-size: 0.813rem; }
    
    /* Premium Button */
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 1.5rem;
        font-size: 0.938rem;
        font-weight: 600;
        letter-spacing: 0.025em;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.5);
    }
    
    /* Stunning Header */
    h1 {
        color: #fff !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        margin-bottom: 1rem !important;
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 50%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(99, 102, 241, 0.3);
    }
    
    /* Premium Messages */
    .msg {
        padding: 1.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        font-size: 0.938rem;
        line-height: 1.7;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        animation: slideUp 0.4s ease;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .msg:hover { transform: translateX(4px); }
    
    .msg-user {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(79, 70, 229, 0.1) 100%);
        border: 1px solid rgba(129, 140, 248, 0.3);
        color: #e0e7ff;
        margin-left: 3rem;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.1);
    }
    
    .msg-ai {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(196, 181, 253, 0.3);
        border-left: 4px solid #a78bfa;
        color: #e0e7ff;
        margin-right: 3rem;
        box-shadow: 0 4px 16px rgba(168, 85, 247, 0.1);
    }
    
    .msg-label {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.75rem;
        opacity: 0.8;
    }
    
    .msg-user .msg-label { color: #a5b4fc; }
    .msg-ai .msg-label { color: #c4b5fd; }
    
    /* Premium Chat Input */
    [data-testid="stChatInput"] {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border: 2px solid rgba(129, 140, 248, 0.3) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: rgba(129, 140, 248, 0.6) !important;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3) !important;
    }
    
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: #e0e7ff !important;
        font-size: 0.938rem !important;
        padding: 1rem !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder { color: #6b7280 !important; }
    
    /* Premium Alerts */
    .stSuccess {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(74, 222, 128, 0.3) !important;
        border-radius: 12px !important;
        color: #86efac !important;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 4px 16px rgba(34, 197, 94, 0.1) !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(248, 113, 113, 0.3) !important;
        border-radius: 12px !important;
        color: #fca5a5 !important;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.1) !important;
    }
    
    /* Premium Image */
    img {
        border-radius: 12px;
        border: 2px solid rgba(129, 140, 248, 0.3);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        transition: all 0.3s;
    }
    
    img:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 32px rgba(99, 102, 241, 0.2);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(129, 140, 248, 0.3), transparent);
        margin: 2.5rem 0;
    }
    
    /* Premium Scrollbar */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.5); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #6366f1, #8b5cf6);
        border-radius: 5px;
    }
    ::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #4f46e5, #7c3aed); }
    
    /* Spinner */
    .stSpinner > div { border-top-color: #6366f1 !important; border-right-color: #8b5cf6 !important; }
    
    /* Hide */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# API
key = os.getenv("GEMINI_API_KEY")
if not key or key == "your_gemini_api_key_here":
    st.error("⚠️ API key required")
    st.stop()

genai.configure(api_key=key)
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Model failed")
    st.stop()

# State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf" not in st.session_state:
    st.session_state.pdf = ""
if "img" not in st.session_state:
    st.session_state.img = None

# Header
st.markdown("# ◆ Monolith AI")
st.markdown('<p style="color: #94a3b8; font-size: 1.125rem; margin-top: -0.75rem; font-weight: 500;">Enterprise intelligence platform • Document analysis • Vision AI • Real-time processing</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("## WORKSPACE")
    
    st.markdown("### Documents")
    pdf = st.file_uploader("", type=['pdf'], key="pdf_upload", label_visibility="collapsed")
    if pdf:
        try:
            reader = PdfReader(pdf)
            st.session_state.pdf = "".join(p.extract_text() for p in reader.pages)
            st.success(f"✓ {len(reader.pages)} pages loaded successfully")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown("### Images")
    img = st.file_uploader("", type=['png','jpg','jpeg','webp'], key="img_upload", label_visibility="collapsed")
    if img:
        try:
            st.session_state.img = Image.open(img)
            st.image(st.session_state.img, use_container_width=True)
            st.success("✓ Image loaded and ready")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    if st.button("Clear Session"):
        st.session_state.messages = []
        st.session_state.pdf = ""
        st.session_state.img = None
        st.rerun()

# Messages
for m in st.session_state.messages:
    if m["role"] == "user":
        st.markdown(f'<div class="msg msg-user"><div class="msg-label">You</div>{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg msg-ai"><div class="msg-label">Monolith AI</div>{m["content"]}</div>', unsafe_allow_html=True)

# Input
prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="msg msg-user"><div class="msg-label">You</div>{prompt}</div>', unsafe_allow_html=True)
    
    with st.spinner("Processing..."):
        try:
            ctx = f"Document context:\n{st.session_state.pdf[:5000]}\n\n" if st.session_state.pdf else ""
            
            if st.session_state.img and any(w in prompt.lower() for w in ['image','picture','photo','see','show','describe','what','analyze','look','view']):
                resp = model.generate_content([ctx + prompt, st.session_state.img])
            else:
                resp = model.generate_content(ctx + prompt)
            
            ans = resp.text
            st.session_state.messages.append({"role": "assistant", "content": ans})
            st.markdown(f'<div class="msg msg-ai"><div class="msg-label">Monolith AI</div>{ans}</div>', unsafe_allow_html=True)
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
