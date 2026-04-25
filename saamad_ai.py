import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. Page Config ---
st.set_page_config(page_title="Sukkur's First AI", page_icon="✨", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b141a; color: white; }
    .user-msg { background-color: #005c4b; padding: 15px; border-radius: 15px 15px 0px 15px; margin-left: auto; width: fit-content; max-width: 75%; margin-bottom: 15px; }
    .ai-msg { background-color: #202c33; padding: 15px; border-radius: 15px 15px 15px 0px; margin-right: auto; width: fit-content; max-width: 75%; margin-bottom: 15px; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Smart Model Loader ---
# Agar 'gemini-1.5-flash' nahi mila, toh ye list mein se doosre try karega
def load_model():
    models_to_try = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']
    for m in models_to_try:
        try:
            model = genai.GenerativeModel(m)
            # Test run to check if it exists
            return model
        except:
            continue
    return None

try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = load_model()
    else:
        st.error("API Key Secrets mein nahi mili!")
except Exception as e:
    st.error(f"Config Error: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. Sidebar ---
with st.sidebar:
    st.title("📸 Sukkur AI Vision")
    uploaded_file = st.file_uploader("Photo upload karein", type=['png', 'jpg', 'jpeg'])
    if st.button("+ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 4. Main Chat Area ---
st.title("Sukkur's First AI")
st.caption("Auto-Switching Engine Active")

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

        if model:
            with st.spinner("Processing..."):
                response = model.generate_content(content_list)
                ai_reply = response.text
            
            st.markdown(f'<div class="ai-msg">{ai_reply}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        else:
            st.error("Google ke sare models busy hain. Thodi der baad try karein.")
            
    except Exception as e:
        st.error(f"Model Error: {e}")
