import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from PIL import Image

# --- 1. CONFIGURATION ---
load_dotenv()
st.set_page_config(
    page_title="Monolith AI", 
    page_icon="◆", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. CSS STYLING (ENTERPRISE THEME) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Inter:wght@400;500&display=swap');
    
    * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
    
    /* Main Background */
    .stApp {
        background-color: #0f1117;
        color: #e2e8f0;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Header Styles */
    h1, h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Custom Title */
    .brand-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .brand-subtitle {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        transition: all 0.3s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1;
        background: rgba(99, 102, 241, 0.05);
    }

    /* Chat Messages */
    .msg-container {
        display: flex;
        flex-direction: column;
        gap: 20px;
        margin-bottom: 100px;
    }
    
    .user-msg {
        align-self: flex-end;
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
        color: #e0e7ff;
        padding: 15px 20px;
        border-radius: 12px;
        max-width: 80%;
        margin-left: auto;
    }
    
    .bot-msg {
        align-self: flex-start;
        background: #1e293b;
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: #cbd5e1;
        padding: 15px 20px;
        border-radius: 12px;
        max-width: 80%;
        margin-right: auto;
    }

    /* Input Field */
    .stTextInput {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 800px;
        z-index: 1000;
    }
    
    .stTextInput input {
        background: rgba(30, 41, 59, 0.95) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 100px !important;
        padding: 22px 30px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    
    /* Padding fix */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        padding-bottom: 120px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. API SETUP ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ API Key missing! Check .env file.")
    st.stop()

genai.configure(api_key=api_key)
# BURASI ONEMLI: Flash modelini kullaniyoruz
model = genai.GenerativeModel('gemini-pro')

# --- 4. FUNCTIONS ---
def get_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# --- 5. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "img_data" not in st.session_state:
    st.session_state.img_data = None

# --- 6. SIDEBAR (WORKSPACE) ---
with st.sidebar:
    st.markdown("### WORKSPACE")
    st.markdown("---")
    
    st.markdown("#### 📄 Documents")
    pdf_file = st.file_uploader("Upload PDF report", type=['pdf'], label_visibility="collapsed")
    if pdf_file:
        try:
            with st.spinner("Indexing document..."):
                st.session_state.pdf_text = get_pdf_text(pdf_file)
            st.success("PDF Loaded")
        except:
            st.error("Error reading PDF")

    st.markdown("#### 📸 Images")
    img_file = st.file_uploader("Upload visual data", type=['png','jpg','jpeg'], label_visibility="collapsed")
    if img_file:
        try:
            st.session_state.img_data = Image.open(img_file)
            st.image(st.session_state.img_data, caption="Visual Input", use_column_width=True)
            st.success("Image Ready")
        except:
            st.error("Error reading Image")
    
    st.markdown("---")
    if st.button("Clear Session"):
        st.session_state.messages = []
        st.session_state.pdf_text = ""
        st.session_state.img_data = None
        st.rerun()

# --- 7. MAIN UI ---

# Header (Only if empty)
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding-top: 10vh; padding-bottom: 40px;">
        <div class="brand-title">◆ Monolith AI</div>
        <div class="brand-subtitle">
            Enterprise Intelligence Platform<br>
            Document Analysis • Vision AI • Real-time Processing
        </div>
    </div>
    """, unsafe_allow_html=True)

# Chat History Display
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg"><b>You</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg"><b>Monolith</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# --- 8. LOGIC CORE ---
if prompt := st.chat_input("Ask anything..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-msg"><b>You</b><br>{prompt}</div>', unsafe_allow_html=True)

    # Bot Logic
    try:
        response_text = ""
        
        # Scenario A: PDF Context
        if st.session_state.pdf_text:
            context = f"DOCUMENT CONTEXT:\n{st.session_state.pdf_text[:10000]}\n\nQUESTION: {prompt}"
            if st.session_state.img_data:
                response = model.generate_content([context, st.session_state.img_data])
            else:
                response = model.generate_content(context)
        
        # Scenario B: Image Context
        elif st.session_state.img_data:
            response = model.generate_content([prompt, st.session_state.img_data])
            
        # Scenario C: Pure Chat
        else:
            # Create proper history format for Gemini
            history_gemini = []
            for m in st.session_state.messages:
                if isinstance(m["content"], str): # Skip if content is not string
                    history_gemini.append({"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]})
            
            # Remove the last user message we just added to session_state, to avoid duplication in history call
            chat = model.start_chat(history=history_gemini[:-1])
            response = chat.send_message(prompt)

        response_text = response.text
        
        # Append Response
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.markdown(f'<div class="bot-msg"><b>Monolith</b><br>{response_text}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"System Error: {e}")