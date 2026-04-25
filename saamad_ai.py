import streamlit as st
from groq import Groq
from gtts import gTTS
from PIL import Image
import base64
import os

# --- 1. Page Configuration (Title and Icon like Gemini) ---
st.set_page_config(page_title="Sammad AI", page_icon="✨", layout="wide")

# --- 2. Ultra-Detailed CSS for Visual Duplicate & Fixed Placement ---
st.markdown("""
<style>
    /* Gemini Dark Theme Root Colors */
    :root { font-family: 'Google Sans', Arial, sans-serif; }
    .main { background-color: #131314; color: #e3e3e3; }
    
    /* Input Bar Style (Chat input area) */
    .stChatInput { border-radius: 30px; background-color: #1e1f20; border: 1px solid #444746; padding: 5px 15px; margin-top: 15px; }
    .stChatInput > div > div > input { background-color: transparent; color: white; font-size: 16px; }

    /* Record Widget styling - making it VERY SMALL */
    .stAudioInput { border: none !important; background-color: transparent !important; width: 40px !important; margin-left: auto; margin-right: auto;}
    .stAudioInput > div > button { background-color: transparent !important; color: #8ab4f8 !important; border-radius: 50%; width: 30px; height: 30px;}

    /* Professional Message Bubbles (Standard look, no heavy color) */
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; padding: 10px 0; max-width: 70%;}
    [data-testid="stChatMessage"] .stMarkdown { border-radius: 12px; font-size: 16px; display: inline-block;}
    
    /* User Message (Right Align, no color tag) */
    [data-testid="stChatMessage-user"] { margin-left: auto; margin-right: 0;}
    [data-testid="stChatMessage-user"] .stMarkdown { background-color: #005c4b; color: white; padding: 12px; }

    /* AI Message (Left Align) */
    [data-testid="stChatMessage-assistant"] { margin-right: auto; margin-left: 0;}
    [data-testid="stChatMessage-assistant"] .stMarkdown { background-color: transparent; color: #e3e3e3; padding: 0 12px; }

    /* Specific Placement for Copy and Voice Buttons */
    .chat-controls { display: flex; align-items: center; gap: 5px; margin-top: 5px; }
    .stButton > button { background-color: transparent !important; border: none !important; color: #e3e3e3 !important; font-size: 18px !important; padding: 0 !important;}
    .stButton > button:hover { color: #8ab4f8 !important;}
</style>
""", unsafe_allow_html=True)

# --- 3. Brain Setup (Using Groq for Text) ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Sammad AI, a sleek visual assistant. Reply in Roman Urdu. Default mode: Text and Photo analysis. Do not include heavy colors or large widgets."}
    ]

# --- 4. Sidebar (Replicated for Gemini Panel look + Photo Feature) ---
with st.sidebar:
    st.title("Sammad AI ✨")
    
    # [FEATURE 4]: + Photo Feature via standard Upload & Direct Capture for browsers
    st.subheader("Photo Input")
    uploaded_image = st.file_uploader("+ Add Photo", type=['png', 'jpg', 'jpeg'], help="Standard Upload or Ctrl+V (if browser supports)")
    
    # Gemini options
    uploaded_audio = st.file_uploader("Upload Audio command", type=['mp3', 'wav', 'm4a'])
    uploaded_doc = st.file_uploader("Upload Document", type=['pdf', 'txt'])
    
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()

# --- 5. Main Chat Area ---
# Professional Title (Gemini style)
st.caption("Powered by Sammad AI ✨ | Groq Brain")

# Display Chat History
for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "image_data" in msg:
             st.image(msg["image_data"], caption="Sent Picture", width=250)

# --- 6. Gemini Hybrid Input Section (Small Mic + Input Bar) ---
st.write("---")

# FEATURE 2: Record line make it VERY small (Choti ungli jitna)
# Centered Small Record Widget
col_r_left, col_r_mid, col_r_right = st.columns([0.45, 0.1, 0.45])
with col_r_mid:
    # 🎙️ SMALL LIVE MIC BUTTON
    recorded_audio = st.audio_input("Rec", help="Voice Command") 

# Main Text Input
user_query = st.chat_input("Ask for anything...")

# Process Input Logic (Text or Photo Analysis)
final_input = user_query
image_to_process = None

# FEATURE 4: Handle Photo Input (Standard Upload for Ctrl+V support)
if uploaded_image:
    final_input = final_input if final_input else "[Analyzing Attached Photo]"
    image_to_process = uploaded_image

# If voice command received
if recorded_audio:
    final_input = " [Voice Command Received - ProcessingSTT is slow]" # Requires proper STT key to make instant

if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})
    if image_to_process:
        # Load and store image data for display history
        pil_image = Image.open(image_to_process)
        st.session_state.messages[-1]["image_data"] = pil_image

    with st.chat_message("user"):
        st.write(final_input)
        if image_to_process:
            st.image(image_to_process, width=250)
        if recorded_audio:
            st.audio(recorded_audio) # Show standard playback for confirmation

    try:
        # For standard Llama on Groq, we handle text analysis. 
        # (Vision models require different Groq key/model)
        # Assuming you want the text model to continue for now.
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        full_response = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.write(full_response)
            
            # --- FEATURE 1 & 5: Placement and Icon only ---
            # Placement using specific CSS in st.markdown below the response
            st.markdown(f'''
                <div class="chat-controls" style="display:flex; justify-content: space-between;">
                    <div style="display:flex; gap: 5px;">
                        <div id="play_btn_holder">
                            <button class="icon-btn" onclick="document.getElementById('audio_src').play()">🔊</button>
                        </div>
                    </div>
                    <div>
                        <div id="copy_btn_holder">
                            <button class="icon-btn" onclick="alert('Text to be copied: {base64.b64encode(full_response.encode()).decode()}')">📋</button>
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            # Hidden Audio Player logic (Hindi tone for Roman Urdu)
            # Changed to require a specific action due to autoplay issues
            if st.button("Generate Audio (Required first)"):
                tts = gTTS(text=full_response[:400], lang='hi') 
                tts.save("reply.mp3")
                with open("reply.mp3", "rb") as f:
                    data = f.read()
                os.remove("reply.mp3")
                b64_audio = base64.b64encode(data).decode()
                st.markdown(f'<audio id="audio_src" src="data:audio/mp3;base64,{b64_audio}"></audio>', unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        st.error(f"Error: {e}")
