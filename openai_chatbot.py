import streamlit as st
import openai
import os

# Simple page setup
st.set_page_config(page_title="AI Chat", page_icon="🤖")

# Simple styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #10a37f;
    font-size: 2.5rem;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

def init_openai():
    """Initialize OpenAI API"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None, "❌ No OpenAI API key found. Please set OPENAI_API_KEY environment variable."

    try:
        openai.api_key = api_key
        return True, "✅ OpenAI API ready"
    except Exception as e:
        return None, f"❌ OpenAI API Error: {e}"

def get_openai_response(message):
    """Get response from OpenAI"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ OpenAI Error: {e}"

# Main interface
st.markdown('<h1 class="main-header">🤖 OpenAI Chat</h1>', unsafe_allow_html=True)

# Check for OpenAI API key
success, message = init_openai()

if not success:
    st.error(message)
    st.info("""
    ### 🔧 **To use OpenAI Chatbot:**

    1. **Get OpenAI API Key:**
       - Go to [OpenAI Platform](https://platform.openai.com/api-keys)
       - Create a new API key

    2. **Set Environment Variable:**
       ```bash
       set OPENAI_API_KEY=your_api_key_here
       ```

    3. **Or modify the code** to use your key directly

    ### 💡 **Free Alternative Options:**
    - **Hugging Face** - Free AI models
    - **Local AI** - Run models on your machine
    - **Other APIs** - Check for free tiers
    """)

    # Simple demo without API
    st.info("💬 **Demo Mode:** You can see the interface, but need an API key to chat.")

    user_message = st.text_input("Enter your message:", placeholder="API key required to chat...")

    if st.button("Send (Demo)") and user_message.strip():
        st.subheader("Your Question:")
        st.write(user_message)
        st.subheader("Response:")
        st.info("🔑 **Please add your OpenAI API key to see actual responses!**")

else:
    st.success(message)

    # Input section
    user_message = st.text_input("Enter your message:", placeholder="Ask me anything...")

    if st.button("Send") and user_message.strip():
        with st.spinner("🤖 Getting response..."):
            response = get_openai_response(user_message.strip())

        st.subheader("Your Question:")
        st.write(user_message)

        st.subheader("AI Response:")
        st.write(response)

# Footer
st.markdown("---")
st.markdown('<center>Powered by OpenAI GPT-3.5 • Built with Streamlit</center>', unsafe_allow_html=True)
