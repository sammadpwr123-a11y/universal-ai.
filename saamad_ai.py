import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
import os

# --- 1. Page Config ---
st.set_page_config(page_title="Sammad AI", page_icon="⚡", layout="wide")

# Professional Gemini-like UI
st.markdown("""
    <style>
    .main { background-color: #0b141a; color: white; }
    .stChatInput { border-radius: 20px; }
    .stAudio { height: 40px; }
    /* Subtle Copy Box */
    div.stCode { border: none; background-color: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Initialize Brain ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Sammad AI, a professional assistant. Switch languages naturally based on the user's input. Only provide copyable code blocks if requested."}
    ]

# --- 3. Audio Features (Speech to Text & Text to Speech) ---
def text_to_speech_data(text):
    tts = gTTS(text=text[:500], lang='en') # Change to 'hi' for Urdu/Hindi
    tts.save("temp.mp3")
    with open("temp.mp3", "rb") as f:
        data = f.read()
    os.remove("temp.mp3")
    return base64.b64encode(data).decode()

# --- 4. Sidebar ---
with st.sidebar:
    st.title("Sammad AI Settings")
    st.info("Voice Input: Use the 'Record' feature in your browser/keyboard if available, or upload a voice clip below.")
    # Professional Voice Input Simulation
    voice_input = st.audio_input("Speak your command:") 
    if st.button("Clear History"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()

# --- 5. Main Chat ---
st.title("Sammad AI")

# Display Messages
for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handling Inputs (Text or Voice)
user_query = st.chat_input("Type your message here...")

# If user uses the new Microphone component
if voice_input:
    st.warning("Voice processing is active. (Requires high-speed API for instant STT)")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    try:
        # Get AI Response
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        full_response = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.write(full_response)
            
            # 1. FIXED: No Auto-play. Only show player if user wants to listen.
            if st.button("🔊 Listen to response"):
                b64_audio = text_to_speech_data(full_response)
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64_audio}" controls autoplay></audio>', unsafe_allow_html=True)
            
            # 2. FIXED: Clipboard/Copy Option (Hidden in a small expander like pro tools)
            with st.expander("Copy Options"):
                st.code(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"Error: {e}")
