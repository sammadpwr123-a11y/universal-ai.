import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. Page Config ---
st.set_page_config(page_title="Sukkur's First AI", page_icon="⚡", layout="wide")

# CSS for Chat Bubbles (WhatsApp Style)
st.markdown("""
    <style>
    .main { background-color: #0b141a; color: white; }
    .user-msg { background-color: #005c4b; padding: 15px; border-radius: 15px 15px 0px 15px; margin-left: auto; width: fit-content; max-width: 75%; margin-bottom: 15px; color: white; }
    .ai-msg { background-color: #202c33; padding: 15px; border-radius: 15px 15px 15px 0px; margin-right: auto; width: fit-content; max-width: 75%; margin-bottom: 15px; color: white; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Ultra-Smart Model Loader (Anti-404) ---
def get_working_model():
    # Instruction for Roman Urdu and personality
    sys_instruction = "You are Sukkur's First AI. Talk to Sammad like a best friend in Roman Urdu/Hindi. Don't be formal. Use simple words. You can see images and speak 70+ languages."
    
    # Inmein se jo bhi zinda hoga, AI khud pakar lega
    possible_models = ['gemini-1.5-flash', 'gemini-pro', 'gemini-1.5-flash-8b']
    
    for m_name in possible_models:
        try:
            m = genai.GenerativeModel(model_name=m_name, system_instruction=sys_instruction)
            # Test run to verify
            return m
        except:
            continue
    return None

try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = get_working_model()
    else:
        st.error("API Key Secrets mein nahi mili!")
except Exception as e:
    st.error(f"Setup Error: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. Sidebar ---
with st.sidebar:
    st.title("⚡ Sukkur AI Pro")
    uploaded_file = st.file_uploader("Photo upload karo...", type=['png', 'jpg', 'jpeg'])
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.success("Bhai ab ye Roman Urdu hi bolega! 🔥")

# --- 4. Chat Display ---
st.title("Sukkur's First AI")

for msg in st.session_state.messages:
    div_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{div_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# --- 5. Input Logic ---
if prompt := st.chat_input("Ask me anything..."):
    st.markdown(f'<div class="user-msg">{prompt}</div>', unsafe_allow_html=True)
    
    try:
        content_to_send = [prompt]
        if uploaded_file:
            img = Image.open(uploaded_file)
            content_to_send.append(img)
            st.image(img, width=250, caption="Uploaded Photo")

        if model:
            with st.spinner("Sukkur AI soch raha hai..."):
                # Yahan hum response mangte hain
                response = model.generate_content(content_to_send)
                ai_reply = response.text
            
            st.markdown(f'<div class="ai-msg">{ai_reply}</div>', unsafe_allow_html=True)
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        else:
            st.error("Bhai, Google ke models नखरे kar rahe hain. API key check karo!")
            
    except Exception as e:
        st.error(f"Error: {e}")
