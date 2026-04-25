import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
import os

# --- 1. Page Configuration (Title and Icon) ---
st.set_page_config(page_title="Sammad AI", page_icon="✨", layout="wide")

# --- 2. Advanced CSS to Duplicated Gemini's Interface ---
st.markdown("""
<style>
    /* Gemini Dark Theme Colors */
    :root { font-family: 'Google Sans', Arial, sans-serif; }
    .main { background-color: #131314; color: #e3e3e3; }
    
    /* Input Bar Style - Gemini look */
    .stChatInput { border-radius: 30px; background-color: #1e1f20; border: 1px solid #444746; padding: 5px 15px; margin-top: 20px; }
    .stChatInput > div > div > input { background-color: transparent; color: white; font-size: 16px; }

    /* Fix the Microphone component look to fit inside the bar area */
    .stAudioInput { border: none !important; background-color: transparent !important; margin-right: 10px; margin-bottom: 0px !important;}
    .stAudioInput > div > button { background-color: transparent !important; color: #8ab4f8 !important; border-radius: 50%; width: 40px; height: 40px;}

    /* Gemini Message Bubbles Style */
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; padding: 10px 0;}
    [data-testid="stChatMessage"] .stMarkdown { border-radius: 12px; font-size: 16px;}
    [data-testid="stChatMessage-user"] .stMarkdown { background-color: #005c4b; color: white; padding: 12px; display: inline-block; float: right; }
    [data-testid="stChatMessage-assistant"] .stMarkdown { background-color: transparent; color: #e3e3e3; padding: 0 12px; }

    /* Hide default upload component borders */
    [data-testid="stFileUploadDropzone"] { border: 1px solid #333; border-radius: 10px; background-color: #1e1f20; }
</style>
""", unsafe_allow_html=True)

# --- 3. Brain Setup (Using Groq) ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Sammad AI, a visual duplicate of Gemini. Reply in Roman Urdu. Only show code blocks if explicitly asked. Keep the UI clean."}
    ]

# --- 4. Sidebar (For File and Voice Uploads - Like Gemini's side panel) ---
with st.sidebar:
    st.title("Sammad AI ✨")
    # Voice File Upload (Optional)
    uploaded_audio = st.file_uploader("Upload an audio command", type=['mp3', 'wav', 'm4a'])
    # Document Upload (Optional)
    uploaded_doc = st.file_uploader("Upload a document", type=['pdf', 'txt'])
    
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()
    st.markdown("---")
    st.write("**Model:** Llama 3.3 70B (Text Master)")

# --- 5. Main Chat Area ---
# No huge titles, just the app name to replicate Gemini's sleek look
st.caption("Now Powered by Llama 3.3 70B (Fast Brain)")

# Display Chat History
for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 6. Gemini-like Hybrid Input Section ---

# First, place the Mic button above the text bar (due to layout limitations)
st.write("---")
col_mic, col_text = st.columns([0.1, 0.9]) # Layout to keep mic button near the bar

with col_mic:
    # 🎙️ LIVE RECORDING BUTTON: Standard Browser-based voice input
    recorded_audio = st.audio_input("Record") 

with col_text:
    user_query = st.chat_input("Type your message here...")

# Handle Input Logic
final_input = user_query
if recorded_audio:
    final_input = " [Voice Command Received]"
if uploaded_audio:
    final_input += " [Uploaded Audio Received]"

if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})
    with st.chat_message("user"):
        st.write(final_input)
        if recorded_audio:
            st.audio(recorded_audio) # Show the recording so you can hear what was sent

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        full_response = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.write(full_response)
            
            # --- FIXED: Manual Options Only ---
            row_btns = st.container()
            with row_btns:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔊 Play Voice"):
                        tts = gTTS(text=full_response[:400], lang='hi') # For Urdu/Hindi tone
                        tts.save("temp.mp3")
                        with open("temp.mp3", "rb") as f:
                            data = f.read()
                        os.remove("temp.mp3")
                        b64 = base64.b64encode(data).decode()
                        st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay style="height:35px;"></audio>', unsafe_allow_html=True)
                with col2:
                    if st.button("📋 Copy Text"):
                        # Only show code if requested, otherwise show raw text for copy
                        st.code(full_response, language=None)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"Error: {e}")
