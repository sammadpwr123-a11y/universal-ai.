import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
import os

# --- 1. Page Config ---
st.set_page_config(page_title="Sammad AI", page_icon="⚡", layout="wide")

# Custom Styling to look like Gemini
st.markdown("""
    <style>
    .main { background-color: #131314; color: #e3e3e3; }
    .stChatInput { border-radius: 20px; border: 1px solid #444; }
    .stChatMessage { background-color: transparent !important; }
    /* Hide the big code block default look */
    div.stCode { border: 1px solid #333; border-radius: 10px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Initialize Brain ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Sammad AI. Reply in Roman Urdu/Hindi by default. Be smart and helpful like Gemini/GPT-4."}
    ]

# --- 3. Audio Generator (Manual Only) ---
def text_to_speech_data(text):
    # Detect if Urdu/Hindi or English for better voice
    tts = gTTS(text=text[:500], lang='hi') 
    tts.save("temp.mp3")
    with open("temp.mp3", "rb") as f:
        data = f.read()
    os.remove("temp.mp3")
    return base64.b64encode(data).decode()

# --- 4. Sidebar (Upload & Voice Fix) ---
with st.sidebar:
    st.title("Sammad AI Settings")
    # Voice Upload instead of live recording to avoid lock-up
    voice_file = st.file_uploader("Upload Voice/Audio Command", type=['mp3', 'wav', 'm4a'])
    file_upload = st.file_uploader("Upload Documents (PDF/Text)", type=['pdf', 'txt'])
    
    if st.button("Clear Chat History"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()

# --- 5. Main Chat Area ---
st.title("Sammad AI")

# Display Messages
for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handling Inputs
if user_query := st.chat_input("Type your message here..."):
    # If audio is uploaded, we add a note
    full_query = user_query
    if voice_file:
        full_query += " [Note: User also uploaded a voice command]"

    st.session_state.messages.append({"role": "user", "content": full_query})
    with st.chat_message("user"):
        st.write(full_query)

    try:
        # Get AI Response
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        ai_reply = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.write(ai_reply)
            
            # Button 1: Audio (Manual)
            if st.button("🔊 Play Voice"):
                b64_audio = text_to_speech_data(ai_reply)
                st.markdown(f'<audio src="data:audio/mp3;base64,{b64_audio}" controls autoplay></audio>', unsafe_allow_html=True)
            
            # Button 2: Copy/Clipboard (Manual)
            if st.button("📋 Show Copy Text"):
                st.code(ai_reply)

        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        
    except Exception as e:
        st.error(f"Error: {e}")
