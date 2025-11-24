# ◆ Monolith AI
### Enterprise Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Gemini AI](https://img.shields.io/badge/Gemini%20AI-8E75B2?style=for-the-badge&logo=google)

**Monolith AI** is a next-generation intelligence platform designed for enterprise-grade document analysis and multi-modal interaction. Built with a sleek **Glassmorphism UI**, it seamlessly integrates **Google's Gemini AI** to provide real-time insights from text, documents, and visual data.

---

## ✨ Features

### 🧠 Multi-modal Chat (Text & Vision)
Engage in natural conversations with an AI that sees what you see. Upload images and ask questions about them in real-time.

### 📄 RAG Support (PDF Document Analysis)
Unlock the knowledge hidden in your documents. Upload PDF reports, contracts, or papers, and let Monolith AI analyze, summarize, and answer questions based on the content.

### 🎨 Glassmorphism UI Design
Experience a modern, premium interface designed for focus and clarity. The dark-themed, translucent aesthetic provides a comfortable and professional workspace.

### 🔒 Secure API Handling
Built with security in mind. API keys are managed securely via environment variables, ensuring your credentials never leak into the codebase.

---

## 🚀 Installation

Follow these steps to set up Monolith AI on your local machine.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/monolith-ai.git
cd monolith-ai
```

### 2. Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the root directory of the project and add your Google Gemini API key:

**File:** `.env`
```ini
GEMINI_API_KEY=your_actual_api_key_here
```
> Don't have a key? Get one from [Google AI Studio](https://aistudio.google.com/).

---

## ⚡ Usage

Launch the application with a single command:

```bash
streamlit run app.py
```

The application will open automatically in your default web browser at `http://localhost:8501`.

---

## 🛠️ Tech Stack

*   **Core:** Python
*   **UI Framework:** Streamlit
*   **AI Model:** Google Gemini Pro & Flash
*   **Document Processing:** PyPDF2
*   **Image Processing:** Pillow

---

© 2024 Monolith AI. All rights reserved.
