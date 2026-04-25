import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
import os

# --- 1. Page Configuration ---
st.set_page_config(page_title="Sukkur's First AI", page_icon="👹", layout="wide")

# Custom CSS for Professional Chat Look
st.markdown("""
    <style>
    .main { background-color: #0b141a; color: white; }
    .user-msg { background-color: #005c4b; padding: 15px; border-radius: 15px 15px 0px 15px; margin-left: auto; width: fit-content; max-width: 70%; margin-bottom: 10px; color: white; }
    .ai-msg { background-color: #202c33; padding: 15px; border-radius: 15px 15px 15px 0px; margin-right: auto; width: fit-content; max-width: 70%; margin-bottom: 10px; color: white; }
    .stTextInput > div > div > input { background-color: #2a3942; color: white; border-radius: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Brain Setup (Groq) ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    # Hum Llama 3.3 70B use kar rahe hain jo bohot fast aur aqalmand hai
    model_id = "llama-3.3-70b-versatile" 
except Exception as e:
    st.error("Groq API Key missing!")

# Personality Injection
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Sukkur's First AI. Talk to Sammad in Roman Urdu/Hindi. Be super smart, act like a pro friend. Use 70+ languages if asked."}
    ]

# --- 3. Advanced Features (Voice) ---
def text_to_audio(text):
    try:
        tts = gTTS(text=text[:500], lang='hi') # Limit to 500 chars for speed
        tts.save("speech.mp3")
        with open("speech.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay style="height:30px;"></audio>'
    except: return ""

# --- 4. Sidebar (File & Settings) ---
with st.sidebar:
    st.title("👹 Ultra AI Control")
    uploaded_file = st.file_uploader("Upload File (PDF/Text)", type=['txt', 'pdf'])
    if st.button("🗑️ Reset Brain"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()
    st.markdown("---")
    st.info("Features: Voice, History, File Reader, Roman Urdu Mode.")

# --- 5. Main Chat Logic ---
st.title("Sukkur's First AI (Ultra Pro)")

# Display history
for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    div_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{div_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# Input
if prompt := st.chat_input("Hukum karein..."):
    # File content check
    file_info = ""
    if uploaded_file:
        file_info = f"\n[User uploaded a file named {uploaded_file.name}]"
        
    st.markdown(f'<div class="user-msg">{prompt}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt + file_info})

    try:
        # Get Response
        response = client.chat.completions.create(
            messages=st.session_state.messages,
            model=model_id,
        )
        ai_reply = response.choices[0].message.content
        
        # Display AI message
        st.markdown(f'<div class="ai-msg">{ai_reply}</div>', unsafe_allow_html=True)
        
        # Audio feature
        audio_html = text_to_audio(ai_reply)
        st.markdown(audio_html, unsafe_allow_html=True)
        
        # Save to session
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
    except Exception as e:
        st.error(f"Groq Error: {e}")
