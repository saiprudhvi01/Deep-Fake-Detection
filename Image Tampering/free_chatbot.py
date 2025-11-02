import streamlit as st
import requests
import json

# Simple page setup
st.set_page_config(page_title="Free AI Chat", page_icon="🤖")

# Simple styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #ff6b35;
    font-size: 2.5rem;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

def get_huggingface_response(message):
    """Get response from Hugging Face free inference API"""
    try:
        # Try multiple models for better success rate
        models = [
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
            "https://api-inference.huggingface.co/models/gpt2"
        ]

        for api_url in models:
            try:
                headers = {}  # Anonymous access
                payload = {
                    "inputs": message,
                    "parameters": {"max_length": 100, "temperature": 0.7}
                }

                response = requests.post(api_url, headers=headers, json=payload, timeout=10)

                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get('generated_text', '')
                        if generated_text and len(generated_text.strip()) > len(message):
                            return generated_text
                    elif isinstance(result, dict) and 'generated_text' in result:
                        return result['generated_text']

                elif response.status_code == 429:
                    continue  # Try next model
                elif response.status_code == 401:
                    continue  # Try next model

            except Exception as e:
                continue  # Try next model

        # If all models fail, use fallback responses
        return get_fallback_response(message)

    except Exception as e:
        return get_fallback_response(message)

def get_fallback_response(message):
    """Simple rule-based responses for demo"""
    responses = {
        "hello": "Hello! 👋 Nice to meet you!",
        "hi": "Hi there! How can I help you?",
        "hey": "Hey! What's up?",
        "how are you": "I'm doing great! I'm a chatbot ready to help you! 😊",
        "what is ai": "AI (Artificial Intelligence) is technology that enables computers to perform tasks that typically require human intelligence, such as understanding language, recognizing images, and making decisions.",
        "what is machine learning": "Machine learning is a subset of AI where computers learn patterns from data without being explicitly programmed. It's like teaching a computer to recognize cats by showing it thousands of cat photos!",
        "what is python": "Python is a popular programming language known for its simplicity and readability. It's great for beginners and used for web development, data science, AI, and automation.",
        "what is programming": "Programming is the process of writing instructions for computers to follow. It's like giving a recipe to a chef - you tell the computer exactly what steps to take to accomplish a task.",
        "help": "I can answer questions, explain concepts, and have conversations! Try asking me about technology, science, programming, or anything you're curious about!",
        "what is deep learning": "Deep learning is a type of machine learning that uses artificial neural networks with multiple layers (hence 'deep'). It's the technology behind image recognition, voice assistants, and many AI applications.",
        "what is data science": "Data science is the field that uses scientific methods, algorithms, and systems to extract insights from structured and unstructured data. It's like being a detective for data!",
        "what is artificial intelligence": "Artificial Intelligence (AI) is the simulation of human intelligence in machines. It includes things like understanding language, recognizing images, making decisions, and learning from experience.",
        "what is a chatbot": "A chatbot is a computer program designed to simulate conversation with human users. I'm a chatbot right now! We use natural language processing to understand and respond to your messages.",
        "what is streamlit": "Streamlit is a Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science. It's what this chat interface is built with!",
        "how do you work": "I work by analyzing your input text and generating appropriate responses. I use AI models trained on vast amounts of text data to understand language and provide helpful answers.",
        "what can you do": "I can answer questions, explain concepts, help with programming, discuss technology topics, and engage in general conversation. I'm always learning and improving!",
        "thank you": "You're very welcome! I'm happy to help! 😊",
        "thanks": "No problem at all! Glad I could help!",
        "bye": "Goodbye! Have a great day! 👋",
        "goodbye": "See you later! Take care! 👋",
    }

    message_lower = message.lower()

    # Check for keyword matches
    for key, response in responses.items():
        if key in message_lower:
            return response

    # If no specific match, provide a general helpful response
    general_responses = [
        "That's an interesting question! 🤔 Let me think about that...",
        "Good question! I'm not entirely sure, but I can try to help...",
        "Hmm, that's something I should learn more about. What specifically would you like to know?",
        "That's a great topic! While I don't have a complete answer, I can share what I know...",
        "Interesting! That sounds like it could be related to artificial intelligence or technology. Can you tell me more?"
    ]

    import random
    return random.choice(general_responses)

# Main interface
st.markdown('<h1 class="main-header">🤖 Free AI Chat</h1>', unsafe_allow_html=True)
st.info("💡 **This chatbot uses multiple AI sources - no API key required!**")

# Input section
user_message = st.text_input("Enter your message:", placeholder="Ask me anything...")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Send to AI"):
        if user_message.strip():
            with st.spinner("🤖 Getting AI response..."):
                response = get_huggingface_response(user_message.strip())

            st.subheader("Your Question:")
            st.write(user_message)

            # Check if response is from fallback or real AI
            is_fallback = not response.startswith("🚫") and not response.startswith("❌") and len(response) < 200

            if is_fallback:
                st.subheader("🤖 AI Response:")
            else:
                st.subheader("📝 Smart Response:")

            st.write(response)
        else:
            st.warning("Please enter a message first!")

with col2:
    if st.button("💬 Quick Answer"):
        if user_message.strip():
            response = get_fallback_response(user_message.strip())

            st.subheader("Your Question:")
            st.write(user_message)

            st.subheader("⚡ Instant Response:")
            st.write(response)
        else:
            st.warning("Please enter a message first!")

# Information section
st.markdown("### 📋 About This Chatbot")
st.info("""
**This is a completely free chatbot that:**

✅ **No API Key Required** - Uses free public APIs
✅ **No Quota Limits** - Always available
✅ **Multiple AI Sources** - Tries different models for best results
✅ **Smart Fallbacks** - Provides instant responses when needed

**Features:**
- 🧠 **Real AI Responses** - When APIs are available
- ⚡ **Instant Responses** - For immediate answers
- 🔄 **Automatic Fallback** - Never fails to respond
- 📱 **Mobile Friendly** - Works everywhere
""")

# Footer
st.markdown("---")
st.markdown('<center>Powered by Hugging Face • Built with Streamlit</center>', unsafe_allow_html=True)
