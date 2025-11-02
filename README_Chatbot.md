# 🤖 Gemini AI Chatbot

A powerful AI chatbot built with Google's Gemini AI and Streamlit.

## ✨ Features

- **Real-time AI Conversations** - Powered by Google Gemini Pro model
- **Conversation Memory** - Maintains context throughout the chat
- **Beautiful UI** - Clean, modern interface with gradient styling
- **Quick Suggestions** - Pre-built prompts for common tasks
- **Chat History Management** - Clear conversation history anytime
- **Responsive Design** - Works on desktop and mobile devices

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key

### Installation

1. **Install dependencies:**
   ```bash
   pip install google-generativeai streamlit
   ```

2. **Get your Gemini API key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Replace the API key in the code

3. **Run the application:**
   ```bash
   streamlit run gemini_chatbot.py
   ```

4. **Open your browser:**
   - Navigate to `http://localhost:8501`

## 🔧 Configuration

### API Key Setup
The API key is already configured in the code:
```python
api_key = "AIzaSyAILWhxauxP3FeYLkktxybdirHwi9ZBB6k"
```

## 💬 Usage

### Basic Chat
1. Type your message in the text area
2. Click "Send Message" or press Enter
3. Wait for Gemini's response
4. Continue the conversation!

### Quick Suggestions
Use the pre-built buttons for common tasks:
- **Explain machine learning** - Learn about ML concepts
- **Help me code in Python** - Get programming assistance
- **Write a creative story** - Generate creative content

### Chat Management
- **Clear History** - Use the sidebar button to reset conversation
- **Context Awareness** - AI remembers previous messages in the conversation

## 🛠️ Technical Details

### Core Technologies
- **Streamlit** - Web application framework
- **Google Generative AI** - Gemini API integration
- **Python** - Core programming language

### Key Functions
- `initialize_gemini()` - Sets up API connection
- `get_gemini_response()` - Handles AI responses and chat history
- `main()` - Main application interface

### Security Notes
- API key is embedded in code (for demo purposes)
- In production, use environment variables or secure key management
- Consider rate limiting for API usage

## 🎨 Customization

### Styling
The app uses custom CSS for beautiful gradients and styling. You can modify:
- Colors and gradients in the CSS section
- Layout and spacing
- Chat bubble designs

### Features
You can extend the chatbot with:
- File upload capabilities
- Image analysis (using Gemini Vision)
- Multi-language support
- Custom personality prompts

## 🔍 Example Conversations

**Technical Questions:**
```
User: Explain quantum computing in simple terms
Gemini: [Detailed explanation with analogies]
```

**Coding Help:**
```
User: Help me write a Python function to calculate fibonacci numbers
Gemini: [Code with explanations and examples]
```

**Creative Tasks:**
```
User: Write a short story about a robot learning to paint
Gemini: [Creative story with engaging narrative]
```

## 📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

Feel free to enhance the chatbot with additional features like:
- Voice input/output
- Multiple AI model selection
- Conversation export
- Advanced chat settings

---

**Built with ❤️ using Google Gemini AI and Streamlit**
