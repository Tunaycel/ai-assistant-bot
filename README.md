# 🤖 AI Assistant Monolith

**Ultimate Intelligence Platform** - A powerful, all-in-one AI assistant combining chat, PDF analysis, and image recognition capabilities. Built with Python, Streamlit, and Google Gemini 1.5 Flash.

## 🚀 Features

### Core Capabilities
- 💬 **Advanced Chat** - Intelligent conversations with context awareness
- 📄 **PDF Analysis** - Extract and analyze text from PDF documents
- 🖼️ **Image Recognition** - AI-powered image analysis and description
- 🎨 **Ultimate Dark Theme** - Modern, sleek monolith design
- ⚡ **Real-time Processing** - Instant responses and analysis
- 🔄 **Multi-modal AI** - Combine text, PDF, and vision in one conversation

### Design Features
- 🌑 Dark mode optimized interface
- 💎 Premium gradient styling
- 📱 Responsive sidebar layout
- ✨ Smooth animations and transitions
- 🎯 Professional file upload system

## 🚀 Installation

### 1. Install Required Packages

```bash
pip install -r requirements.txt
```

### 2. Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key

### 3. Set Environment Variables

Create a `.env` file in the project directory and add:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace `your_gemini_api_key_here` with your actual API key.

## 🎮 Usage

Run this command in your terminal to start the application:

```bash
streamlit run app.py
```

Your browser will automatically open `http://localhost:8501`.

## 💡 How to Use

### 📄 PDF Analysis
1. Click **"PDF Document"** in the sidebar
2. Upload your PDF file
3. Ask questions about the document content
4. Example: *"Summarize the main points from this PDF"*

### 🖼️ Image Analysis
1. Click **"Image Analysis"** in the sidebar
2. Upload an image (PNG, JPG, JPEG, WebP)
3. Ask questions about the image
4. Example: *"What's in this image?"* or *"Describe this picture"*

### 💬 General Chat
1. Simply type your question in the chat input
2. Get intelligent responses from Gemini AI
3. Context from uploaded files is automatically included

### 🔄 Multi-Modal Queries
- Upload both PDF and image
- Ask questions that combine information from both
- Clear all data with one click to start fresh

## 📁 Project Structure

```
ai-assistant-bot/
│
├── app.py              # Main Monolith application with all features
├── requirements.txt    # Python dependencies (Streamlit, Gemini, PyPDF2, Pillow)
├── .env               # Environment variables (create this with your API key)
├── .gitignore         # Git ignore file (protects .env)
└── README.md          # Documentation
```

## 🎨 UI Features

### Ultimate Monolith Design
- **Dark Theme**: Professional black/dark blue gradient background
- **Neon Accents**: Cyan (#00d4ff) and purple (#bb86fc) highlights
- **Animated Chat**: Smooth slide-in animations for messages
- **Sidebar Integration**: All file uploads in organized sidebar
- **Modern Typography**: Bold, clean fonts with proper spacing
- **Responsive Layout**: Adapts to different screen sizes

## 🔒 Security Notes

- Never share or commit your `.env` file to git
- Keep your API key private
- Monitor your usage limits

## 🛠️ Technologies

- **Python 3.8+** - Core programming language
- **Streamlit** - Modern web interface framework
- **Google Gemini 1.5 Flash** - Advanced AI model (text + vision)
- **PyPDF2** - PDF text extraction and analysis
- **Pillow (PIL)** - Image processing and handling
- **python-dotenv** - Secure environment variable management

## 📝 License

This project is for educational purposes and free to use.

## 🤝 Contributing

Feel free to submit pull requests with your suggestions and contributions!

## ⚠️ Troubleshooting

### "Gemini API key not found" error
- Make sure the `.env` file is in the project directory
- Verify the API key is correctly copied
- Check that the file name is exactly `.env`
- Ensure the key starts with `AIza...`

### PDF Upload Issues
- Ensure the file is a valid PDF format
- Check that the PDF is not password-protected
- Try with a smaller PDF if you encounter memory issues

### Image Upload Issues
- Supported formats: PNG, JPG, JPEG, WebP
- Make sure the image file is not corrupted
- Try reducing image size if upload fails

### "API rate limit" error
- Ensure you have sufficient quota in your Google Cloud account
- Wait a moment if you've exceeded the rate limit
- Check your usage at [Google AI Studio](https://aistudio.google.com/)

### Model Not Responding
- Check your internet connection
- Verify Google AI services are operational
- Try clearing chat and restarting the app

---

💻 **Happy Building with Ultimate Monolith!** 🤖⚡

