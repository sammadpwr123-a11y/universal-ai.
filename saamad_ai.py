import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. Page Config ---
st.set_page_config(page_title="Sukkur's First AI", page_icon="✨", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #131314; color: #e3e3e3; }
    .user-msg { background-color: #005c4b; padding: 15px; border-radius: 15px 15px 0px 15px; margin-left: auto; width: fit-content; max-width: 75%; margin-bottom: 15px; }
    .ai-msg { background-color: #1e1f20; padding: 15px; border-radius: 15px 15px 15px 0px; margin-right: auto; width: fit-content; max-width: 75%; margin-bottom: 15px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Setup Gemini Engine ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # FIX: Model ka naam 'models/' ke saath likha hai taake 404 na aaye
        model = genai.GenerativeModel('models/gemini-1.5-flash')
    else:
        st.error("API Key Secrets mein nahi mili!")
except Exception as e:
    st.error(f"Configuration Error: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. Sidebar ---
with st.sidebar:
    st.title("📸 Sukkur AI Vision")
    uploaded_file = st.file_uploader("Photo yahan upload karein", type=['png', 'jpg', 'jpeg'])
    if st.button("+ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 4. Main Chat Area ---
st.title("Sukkur's First AI")
st.caption("Now Powered by Gemini 1.5 Flash")

for msg in st.session_state.messages:
    div_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{div_class}">{msg["content"]}</div>', unsafe_allow_html=True)

if prompt := st.chat_input("Ask for anything..."):
    st.markdown(f'<div class="user-msg">{prompt}</div>', unsafe_allow_html=True)
    
    try:
        content_list = [prompt]
        if uploaded_file:
            img = Image.open(uploaded_file)
            content_list.append(img)
            st.image(img, width=250)

        # Generating Response
        with st.spinner("Soch raha hoon..."):
            response = model.generate_content(content_list)
            ai_reply = response.text
        
        st.markdown(f'<div class="ai-msg">{ai_reply}</div>', unsafe_allow_html=True)
        
        # Save History
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
    except Exception as e:
        # Error detail dikhane ke liye
        st.error(f"Model Error: {e}")
