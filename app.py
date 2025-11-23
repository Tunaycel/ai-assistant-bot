import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Assistant Monolith",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultimate Monolith Dark Theme CSS
st.markdown("""
    <style>
    /* Main Background - Ultimate Dark */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0f0f23 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16213e 0%, #0f0f23 100%);
        border-right: 2px solid #00d4ff;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label {
        color: #00d4ff !important;
        font-weight: 600;
    }
    
    /* Chat Messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border-left: 5px solid;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        animation: slideIn 0.4s ease-out;
        backdrop-filter: blur(10px);
    }
    
    .user-message {
        background: linear-gradient(135deg, #1e3a5f 0%, #2a4d7c 100%);
        border-left-color: #00d4ff;
        color: #ffffff;
        margin-left: 3rem;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #2d1b4e 0%, #3d2963 100%);
        border-left-color: #bb86fc;
        color: #e0e0e0;
        margin-right: 3rem;
    }
    
    .system-message {
        background: linear-gradient(135deg, #1a3a1a 0%, #2d4d2d 100%);
        border-left-color: #4caf50;
        color: #ffffff;
        text-align: center;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Header Styling */
    .main-header {
        text-align: center;
        color: #00d4ff;
        font-size: 3.5rem;
        font-weight: 900;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        margin-bottom: 0.5rem;
        letter-spacing: 2px;
    }
    
    .subtitle {
        text-align: center;
        color: #bb86fc;
        font-size: 1.3rem;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    
    /* File Upload Styling */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed #00d4ff;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        color: #000000;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 2rem;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00ffff 0%, #00d4ff 100%);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.6);
        transform: translateY(-2px);
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border: 2px solid #00d4ff;
        border-radius: 10px;
    }
    
    /* Success/Info Messages */
    .stSuccess, .stInfo {
        background: rgba(0, 212, 255, 0.1);
        border-left: 5px solid #00d4ff;
        color: #00d4ff;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #00d4ff;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(0, 212, 255, 0.1);
        color: #00d4ff;
        border-radius: 10px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# API key check
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key or gemini_api_key == "your_gemini_api_key_here":
    st.error("⚠️ Gemini API key not found!")
    st.warning("Please set GEMINI_API_KEY in your .env file")
    st.stop()

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

# Initialize models
try:
    text_model = genai.GenerativeModel('gemini-1.5-flash')
    vision_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"❌ Error initializing models: {str(e)}")
    st.stop()

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "current_image" not in st.session_state:
    st.session_state.current_image = None

# Header
st.markdown('<h1 class="main-header">🤖 AI ASSISTANT MONOLITH</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ultimate Intelligence • PDF Analysis • Vision • Chat</p>', unsafe_allow_html=True)

# Sidebar - File Upload Section
with st.sidebar:
    st.markdown("### 📁 FILE UPLOAD CENTER")
    st.markdown("---")
    
    # PDF Upload Section
    st.markdown("#### 📄 PDF Document")
    uploaded_pdf = st.file_uploader(
        "Upload PDF file",
        type=['pdf'],
        help="Upload a PDF document to analyze its content"
    )
    
    if uploaded_pdf:
        try:
            pdf_reader = PdfReader(uploaded_pdf)
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
            
            st.session_state.pdf_text = pdf_text
            st.success(f"✅ PDF loaded: {len(pdf_reader.pages)} pages")
            
            with st.expander("📖 View PDF Content"):
                st.text_area("Content", pdf_text[:1000] + "...", height=200, disabled=True)
        except Exception as e:
            st.error(f"❌ Error reading PDF: {str(e)}")
    
    st.markdown("---")
    
    # Image Upload Section
    st.markdown("#### 🖼️ Image Analysis")
    uploaded_image = st.file_uploader(
        "Upload Image file",
        type=['png', 'jpg', 'jpeg', 'webp'],
        help="Upload an image to analyze with AI vision"
    )
    
    if uploaded_image:
        try:
            image = Image.open(uploaded_image)
            st.session_state.current_image = image
            st.image(image, caption="Uploaded Image", use_container_width=True)
            st.success("✅ Image loaded successfully")
        except Exception as e:
            st.error(f"❌ Error loading image: {str(e)}")
    
    st.markdown("---")
    
    # Clear All Button
    if st.button("🗑️ CLEAR ALL DATA", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pdf_text = ""
        st.session_state.current_image = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("""
    ### 💡 TIPS
    - Upload PDF for document analysis
    - Upload images for visual AI
    - Ask questions about uploaded content
    - Combine text and vision queries
    """)

# Main Chat Area
st.markdown("### 💬 CONVERSATION")

# Display chat history
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 YOU</strong><br><br>
                {content}
            </div>
        """, unsafe_allow_html=True)
    elif role == "assistant":
        st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 AI ASSISTANT</strong><br><br>
                {content}
            </div>
        """, unsafe_allow_html=True)
    elif role == "system":
        st.markdown(f"""
            <div class="chat-message system-message">
                <strong>⚡ SYSTEM</strong><br><br>
                {content}
            </div>
        """, unsafe_allow_html=True)

# User input
user_input = st.chat_input("🎯 Type your message here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 YOU</strong><br><br>
            {user_input}
        </div>
    """, unsafe_allow_html=True)
    
    # Process with AI
    with st.spinner("🧠 AI is processing..."):
        try:
            # Prepare context
            context = ""
            
            # Add PDF context if available
            if st.session_state.pdf_text:
                context += f"\n\n[PDF CONTENT]\n{st.session_state.pdf_text[:3000]}\n"
            
            # Handle image analysis
            if st.session_state.current_image and ("image" in user_input.lower() or "picture" in user_input.lower() or "photo" in user_input.lower() or "what" in user_input.lower()):
                # Use vision model for image
                response = vision_model.generate_content([user_input, st.session_state.current_image])
                assistant_message = response.text
            else:
                # Use text model with context
                prompt = f"{context}\n\nUser Question: {user_input}"
                response = text_model.generate_content(prompt)
                assistant_message = response.text
            
            # Add AI response
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            
            # Display AI response
            st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 AI ASSISTANT</strong><br><br>
                    {assistant_message}
                </div>
            """, unsafe_allow_html=True)
            
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Please check your API key and try again.")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; color: #00d4ff;'>
        <p><strong>⚡ ULTIMATE MONOLITH ⚡</strong></p>
        <p>Powered by Google Gemini 1.5 Flash | Built with Python & Streamlit</p>
    </div>
    """, unsafe_allow_html=True)
