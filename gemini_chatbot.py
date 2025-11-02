import streamlit as st
import google.generativeai as genai

# Try to import PaLM API as fallback
try:
    import google.generativeai as palm
    PALM_AVAILABLE = True
except ImportError:
    PALM_AVAILABLE = False

# Simple page setup
st.set_page_config(page_title="Gemini Chat", page_icon="🤖")

# Simple styling
st.markdown("""
<style>
body {
    background: #f0f2f5;
}
.main-header {
    text-align: center;
    color: #1f77b4;
    font-size: 2.5rem;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

def init_gemini():
    try:
        genai.configure(api_key="AIzaSyAILWhxauxP3FeYLkktxybdirHwi9ZBB6k")

        # First try to list available models
        try:
            st.info("🔍 Checking available models...")
            models = genai.list_models()
            available_models = [model.name for model in models if 'generateContent' in model.supported_generation_methods]

            st.info(f"📋 Available models: {available_models}")

            # Try the first available model
            if available_models:
                model_name = available_models[0].replace('models/', '')
                st.success(f"✅ Using model: {model_name}")
                return genai.GenerativeModel(model_name)

        except Exception as e:
            st.warning(f"Could not list models: {e}")

        # Try different model names
        model_names = ['gemini', 'models/gemini', 'text-bison-001', 'chat-bison-001']

        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                st.success(f"✅ Connected to {model_name}")
                return model
            except Exception as e:
                st.warning(f"❌ {model_name} not available: {str(e)}")
                continue

        # Try PaLM API as fallback
        try:
            st.info("🔄 Trying PaLM API...")
            if PALM_AVAILABLE:
                palm.configure(api_key="AIzaSyAILWhxauxP3FeYLkktxybdirHwi9ZBB6k")
                model = palm.GenerativeModel('models/chat-bison-001')
                st.success("✅ Connected to PaLM API")
                return model
            else:
                st.warning("PaLM API not available")
        except Exception as e:
            st.warning(f"PaLM API failed: {e}")

        st.error("❌ No available models found")
        return None

    except Exception as e:
        st.error(f"API Configuration Error: {e}")
        return None

def get_response(model, message):
    try:
        # Try Gemini API first
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        error_message = str(e)

        # Check if it's a quota exceeded error
        if "quota" in error_message.lower() or "429" in error_message or "exceeded" in error_message.lower():
            return """🚫 **API Quota Exceeded**

Your free Gemini API quota has been used up. Here's what you can do:

### 🔄 **Wait for Reset**
- Free quotas usually reset **daily** (in 24 hours)
- Try again tomorrow for fresh quota

### 💳 **Upgrade Options**
1. **Google AI Studio** - Get more quota
2. **Paid Plan** - Higher limits and priority access
3. **Different API Key** - If you have another key with remaining quota

### 🔗 **Useful Links**
- [Check Your Usage](https://ai.dev/usage?tab=rate-limit)
- [Rate Limits Documentation](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Pricing Plans](https://ai.google.dev/pricing)

### 🤖 **Alternative Options**
- **OpenAI GPT** - If you have an OpenAI API key
- **Local AI** - Run AI models locally
- **Other AI APIs** - Claude, Hugging Face, etc.

**Please try again in 24 hours or upgrade your plan!** ⏰"""

        # Try PaLM API if Gemini fails
        try:
            if hasattr(model, 'generate_text'):
                response = model.generate_text(message)
                # PaLM API response format might be different
                if hasattr(response, 'text'):
                    return response.text
                elif hasattr(response, 'result'):
                    return response.result
                else:
                    return str(response)
            else:
                return f"Error: {e}. Model may not support generate_content."
        except Exception as e2:
            return f"Both Gemini and PaLM APIs failed: {e}, {e2}"

# Main interface
st.markdown('<h1 class="main-header">🤖 Gemini AI Chat</h1>', unsafe_allow_html=True)

model = init_gemini()

if model is None:
    st.error("❌ Could not connect to Gemini API")
    st.stop()

# Input section
user_message = st.text_input("Enter your message:", placeholder="Type your question here...")

if st.button("Send") and user_message.strip():
    with st.spinner("Getting response..."):
        response = get_response(model, user_message.strip())

    st.subheader("Your Question:")
    st.write(user_message)

    st.subheader("Gemini's Answer:")
    st.write(response)

# Simple footer
st.markdown("---")
st.markdown('<center>Powered by Google Gemini AI</center>', unsafe_allow_html=True)
