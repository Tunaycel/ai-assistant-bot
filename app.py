import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import PyPDF2

# --- 1. CONFIGURATION ---
load_dotenv()
st.set_page_config(
    page_title="Monolith AI", 
    page_icon="◆", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. CSS STYLING ---
st.markdown("""
<style>
    /* --- FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    /* --- GLOBAL VARIABLES --- */
    :root {
        --bg-color: #050509;
        --sidebar-bg: rgba(10, 10, 15, 0.7);
        --glass-border: rgba(255, 255, 255, 0.08);
        --accent-primary: #6366f1; /* Indigo */
        --accent-secondary: #a855f7; /* Purple */
        --accent-glow: #3b82f6; /* Blue */
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
    }

    /* --- MAIN APP CONTAINER --- */
    .stApp {
        background-color: var(--bg-color);
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 85% 30%, rgba(168, 85, 247, 0.08) 0%, transparent 50%);
        color: var(--text-primary);
        font-family: 'Outfit', sans-serif;
    }

    /* --- SIDEBAR --- */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid var(--glass-border);
        box-shadow: 10px 0 30px rgba(0,0,0,0.2);
    }
    
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: var(--text-primary);
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* --- TYPOGRAPHY --- */
    h1, h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .brand-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 40px rgba(255,255,255,0.1);
    }
    
    .brand-subtitle {
        color: var(--text-secondary);
        font-size: 1.2rem;
        font-weight: 400;
        letter-spacing: 0.5px;
        margin-bottom: 4rem;
        background: rgba(255,255,255,0.03);
        padding: 10px 20px;
        border-radius: 100px;
        border: 1px solid var(--glass-border);
        display: inline-block;
    }

    /* --- CHAT MESSAGES --- */
    .user-msg {
        align-self: flex-end;
        background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
        color: white;
        padding: 18px 24px;
        border-radius: 24px 24px 4px 24px;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.2);
        max-width: 75%;
        margin-left: auto;
        font-size: 1rem;
        line-height: 1.6;
        border: 1px solid rgba(255,255,255,0.1);
        animation: slideInRight 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
    
    .bot-msg {
        align-self: flex-start;
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        color: #e2e8f0;
        padding: 18px 24px;
        border-radius: 24px 24px 24px 4px;
        max-width: 75%;
        margin-right: auto;
        font-size: 1rem;
        line-height: 1.6;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        animation: slideInLeft 0.4s cubic-bezier(0.2, 0.8, 0.2, 1);
    }

    /* --- INPUT FIELD --- */
    .stTextInput {
        position: fixed;
        bottom: 40px;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 750px;
        z-index: 1000;
    }
    
    .stTextInput > div > div > input {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 100px !important;
        padding: 24px 35px !important;
        font-size: 1.05rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 0 0 2px rgba(99, 102, 241, 0.3);
        transform: translateY(-2px);
    }

    /* --- FILE UPLOADER --- */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.02);
        border: 1px dashed rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        background: rgba(99, 102, 241, 0.05);
        border-color: var(--accent-primary);
        transform: scale(1.01);
    }
    
    /* --- ANIMATIONS --- */
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    /* --- UTILS --- */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] { padding-bottom: 140px; }
</style>
""", unsafe_allow_html=True)

# --- 3. API & AUTO MODEL SELECTION ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ API Key missing! Check .env file.")
    st.stop()

genai.configure(api_key=api_key)

# --- YENI YONTEM: OTOMATIK MODEL BULUCU ---
@st.cache_resource
def get_working_model():
    """Sistemde calisan ilk modeli otomatik bulur ve test eder"""
    debug_logs = []
    try:
        # Genisletilmis model listesi (Oncelik sirasi)
        candidate_models = [
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro',
            'gemini-1.5-flash-latest',
            'gemini-1.5-pro-latest',
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro',
            'models/gemini-pro'
        ]
        
        # API'den erisilebilir modelleri cekmeye calis
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    if m.name not in candidate_models:
                        candidate_models.append(m.name)
        except Exception as e:
            debug_logs.append(f"List models failed: {str(e)}")

        # Sirayla modelleri dene ve CALISANI dondur
        for model_name in candidate_models:
            try:
                model = genai.GenerativeModel(model_name)
                # Test atisi yap (Modelin gercekten calistigini dogrula)
                model.generate_content("test")
                return model, debug_logs
            except Exception as e:
                debug_logs.append(f"{model_name}: {str(e)}")
                continue
                
        return None, debug_logs
    except Exception as e:
        debug_logs.append(f"Critical Error: {str(e)}")
        return None, debug_logs

# Modeli yukle
model, debug_info = get_working_model()

# Eger hicbir model bulunamazsa hata ver
if not model:
    st.error("❌ System Error: No compatible Gemini model found.")
    with st.expander("Debug Info (Please share this)", expanded=True):
        st.write("API Key Status:", "Present" if api_key else "Missing")
        for log in debug_info:
            st.code(log)
    st.stop()

# --- 4. FUNCTIONS ---
def get_pdf_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
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

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg"><b>You</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg"><b>Monolith</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# --- 8. LOGIC CORE ---
if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-msg"><b>You</b><br>{prompt}</div>', unsafe_allow_html=True)

    try:
        response_text = ""
        
        if st.session_state.pdf_text:
            context = f"DOCUMENT CONTEXT:\n{st.session_state.pdf_text[:10000]}\n\nQUESTION: {prompt}"
            # Bazi modeller resim+pdf ayni anda desteklemeyebilir, guvenli kullanim:
            try:
                if st.session_state.img_data:
                    response = model.generate_content([context, st.session_state.img_data])
                else:
                    response = model.generate_content(context)
            except:
                # Fallback: Sadece metin dene
                response = model.generate_content(context)

        elif st.session_state.img_data:
             response = model.generate_content([prompt, st.session_state.img_data])
            
        else:
            # Standart sohbet
            chat = model.start_chat(history=[{"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]} for m in st.session_state.messages if isinstance(m["content"], str)][:-1])
            response = chat.send_message(prompt)

        response_text = response.text
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.markdown(f'<div class="bot-msg"><b>Monolith</b><br>{response_text}</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"System Error: {e}")