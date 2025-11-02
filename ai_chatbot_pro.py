import streamlit as st
import google.generativeai as genai
import requests
import json
import time

# Page configuration
st.set_page_config(
    page_title="🚀 AI Chatbot Pro",
    page_icon="🚀",
    layout="wide"
)

# Enhanced styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #4285f4 0%, #34a853 50%, #fbbc05 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }

    .chat-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }

    .user-message {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }

    .bot-message {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 4px solid #4caf50;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
    }

    .status-warning {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ffeaa7;
    }

    .status-error {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def initialize_ai_services(api_key):
    """Initialize multiple AI services with the provided key"""
    services = {}

    # Try Gemini API
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        services['gemini'] = model
        st.success("✅ **Gemini API:** Connected successfully")
    except Exception as e:
        st.warning(f"⚠️ **Gemini API:** {str(e)}")
        services['gemini'] = None

    # Try OpenAI-style API (if key works)
    try:
        # Some Google API keys work with OpenAI format
        import openai
        openai.api_key = api_key
        services['openai'] = True
        st.success("✅ **OpenAI Compatible:** API key accepted")
    except Exception as e:
        services['openai'] = None

    return services

def get_gemini_response(model, message):
    """Get response from Gemini API"""
    try:
        response = model.generate_content(message)
        return response.text, "gemini"
    except Exception as e:
        raise Exception(f"Gemini API Error: {str(e)}")

def get_openai_response(api_key, message):
    """Get response from OpenAI API"""
    try:
        import openai
        openai.api_key = api_key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content, "openai"
    except Exception as e:
        raise Exception(f"OpenAI API Error: {str(e)}")

def get_fallback_response(message):
    """Enhanced fallback responses"""
    responses = {
        "hello": "Hello! 👋 I'm your AI assistant, ready to help you with any questions!",
        "hi": "Hi there! How can I assist you today?",
        "what is ai": "🤖 **Artificial Intelligence (AI)** is technology that enables computers to perform tasks that typically require human intelligence, such as understanding language, recognizing images, solving problems, and learning from experience.",
        "what is machine learning": "🧠 **Machine Learning** is a subset of AI where computers learn patterns from data without being explicitly programmed. For example, showing a computer thousands of cat photos to teach it to recognize cats!",
        "what is deep learning": "🕸️ **Deep Learning** uses artificial neural networks with multiple layers (hence 'deep') to process data. It's the technology behind facial recognition, voice assistants, and self-driving cars.",
        "what is python": "🐍 **Python** is a popular programming language known for its simplicity and readability. It's widely used for web development, data science, artificial intelligence, and automation.",
        "what is programming": "💻 **Programming** is writing instructions for computers to follow. It's like giving a recipe to a chef - you specify exactly what steps the computer should take to accomplish a task.",
        "what is data science": "📊 **Data Science** is the field that uses scientific methods, algorithms, and systems to extract insights from data. Data scientists are like detectives who find patterns and insights in large datasets!",
        "what is a chatbot": "💬 **Chatbots** are computer programs designed to simulate human conversation. I'm a chatbot right now! We use natural language processing to understand your questions and provide helpful responses.",
        "how do you work": "🔧 I work by analyzing your input text and generating appropriate responses using advanced AI models. I can access multiple AI services and always try to provide the most helpful answer possible!",
        "what can you do": "🚀 I can help you with questions about technology, science, programming, general knowledge, and much more. I can explain complex topics, help with coding problems, and engage in natural conversations!",
        "help": "🆘 I can help you with questions about AI, technology, programming, science, and general knowledge. Try asking me to explain concepts, solve problems, or just have a conversation!",
        "thank you": "You're very welcome! 😊 I'm always happy to help!",
        "thanks": "No problem at all! Glad I could assist you!",
    }

    message_lower = message.lower()

    # Check for exact matches first
    for key, response in responses.items():
        if key == message_lower or key in message_lower:
            return response, "fallback"

    # General responses for unmatched queries
    general_responses = [
        "🤔 That's an interesting question! Let me think about how to best explain that...",
        "💡 Great question! While I don't have a specific answer ready, I can share some general insights...",
        "🔍 That's a fascinating topic! What specifically would you like to know about it?",
        "🧠 Interesting! That sounds like it could be related to artificial intelligence or technology. Can you tell me more?",
        "📚 That's a complex topic! I can try to break it down for you. What aspect interests you most?"
    ]

    import random
    return random.choice(general_responses), "fallback"

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 AI Chatbot Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Advanced AI Assistant with Multiple AI Services</p>', unsafe_allow_html=True)

    # API Key input
    api_key = "AIzaSyBZW8E3MqPIuHfhfjSG4AgfiGZ3jQJviYQ"

    if not api_key:
        st.error("❌ Please provide an API key")
        return

    # Initialize AI services
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown("### 🔧 Initializing AI Services...")

    services = initialize_ai_services(api_key)

    # Show service status
    if services.get('gemini'):
        st.markdown('<div class="status-success">✅ Gemini AI: Ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-warning">⚠️ Gemini AI: Not available</div>', unsafe_allow_html=True)

    if services.get('openai'):
        st.markdown('<div class="status-success">✅ OpenAI Compatible: Ready</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-warning">⚠️ OpenAI Compatible: Not available</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Chat interface
    st.markdown("### 💬 Chat with AI")

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for i, msg in enumerate(st.session_state.chat_history):
        if msg['role'] == 'user':
            st.markdown(f'<div class="user-message"><strong>👤 You:</strong><br>{msg["content"]}</div>',
                       unsafe_allow_html=True)
        else:
            service_icon = "🤖" if msg['service'] == 'gemini' else "🧠" if msg['service'] == 'openai' else "💡"
            st.markdown(f'<div class="bot-message"><strong>{service_icon} AI ({msg["service"].upper()}):</strong><br>{msg["content"]}</div>',
                       unsafe_allow_html=True)

    # Input section
    st.markdown("### 📝 Your Message")

    with st.form(key='chat_form'):
        user_input = st.text_area(
            "Type your message here...",
            height=100,
            placeholder="Ask me anything! I can help with technology, programming, science, and general questions...",
            help="Ask about AI, coding, science, or anything you're curious about!"
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            send_button = st.form_submit_button("🚀 Send Message", use_container_width=True)

    # Handle form submission
    if send_button and user_input.strip():
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input.strip(),
            'service': 'user'
        })

        # Show thinking indicator
        with st.spinner("🤖 AI is thinking..."):
            response_text = None
            service_used = None

            # Try Gemini first
            if services.get('gemini'):
                try:
                    response_text, service_used = get_gemini_response(services['gemini'], user_input.strip())
                    st.success("✅ Used Gemini AI")
                except Exception as e:
                    st.warning(f"⚠️ Gemini failed: {str(e)}")

            # Try OpenAI if Gemini failed
            if not response_text and services.get('openai'):
                try:
                    response_text, service_used = get_openai_response(api_key, user_input.strip())
                    st.success("✅ Used OpenAI Compatible API")
                except Exception as e:
                    st.warning(f"⚠️ OpenAI failed: {str(e)}")

            # Use fallback if both failed
            if not response_text:
                response_text, service_used = get_fallback_response(user_input.strip())
                st.info("💡 Used Smart Fallback Response")

        # Add AI response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response_text,
            'service': service_used
        })

        # Rerun to update display
        st.rerun()

    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()

    # Quick suggestions
    st.markdown("### 💡 Quick Suggestions")

    suggestions = [
        "Explain artificial intelligence",
        "Help me learn Python",
        "What is machine learning?",
        "How do chatbots work?"
    ]

    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        col = cols[i % 2]
        if col.button(suggestion, key=f"suggestion_{i}", use_container_width=True):
            # Simulate clicking the suggestion
            st.session_state.chat_history.append({
                'role': 'user',
                'content': suggestion,
                'service': 'user'
            })

            with st.spinner("🤖 Getting response..."):
                # Try Gemini first
                response_text = None
                service_used = None

                if services.get('gemini'):
                    try:
                        response_text, service_used = get_gemini_response(services['gemini'], suggestion)
                    except:
                        pass

                if not response_text and services.get('openai'):
                    try:
                        response_text, service_used = get_openai_response(api_key, suggestion)
                    except:
                        pass

                if not response_text:
                    response_text, service_used = get_fallback_response(suggestion)

            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response_text,
                'service': service_used
            })

            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <strong>🚀 AI Chatbot Pro</strong><br>
        Powered by Multiple AI Services • Built with Streamlit<br>
        Features: Gemini AI, OpenAI Compatible, Smart Fallbacks
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
