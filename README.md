# 🤖 AI Chatbot Application

A modern AI chatbot application built with Python and Streamlit. Powered by Google's advanced Gemini Pro model.

## 📋 Features

- ✨ Modern and user-friendly interface
- 🎨 Gradient background and custom design
- 💬 Real-time chat experience
- 📝 Conversation history tracking
- 🗑️ Clear chat functionality
- 🎯 Powered by Google Gemini Pro model

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

## 💡 Usage Tips

1. **Ask Clear Questions**: Express your question clearly and precisely
2. **Provide Context**: Give additional information for more detailed answers
3. **Use Clear Chat**: Click the button to start a fresh conversation

## 📁 Project Structure

```
ai-bot/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (you need to create this)
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## 🔒 Security Notes

- Never share or commit your `.env` file to git
- Keep your API key private
- Monitor your usage limits

## 🛠️ Technologies

- **Python 3.8+**
- **Streamlit**: Web interface
- **Google Gemini API**: AI model integration
- **python-dotenv**: Environment variable management

## 📝 License

This project is for educational purposes and free to use.

## 🤝 Contributing

Feel free to submit pull requests with your suggestions and contributions!

## ⚠️ Troubleshooting

### "Gemini API key not found" error
- Make sure the `.env` file is in the project directory
- Verify the API key is correctly copied
- Check that the file name is exactly `.env`

### "API rate limit" error
- Ensure you have sufficient quota in your Google Cloud account
- Wait a moment if you've exceeded the rate limit

### Connection error
- Check your internet connection
- Verify Google AI services are operational

---

💻 **Happy Chatting!** 🤖

