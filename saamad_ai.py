import streamlit as st
from groq import Groq
from gtts import gTTS
import base64

# --- 1. Page Configuration (A to Z English) ---
st.set_page_config(page_title="Sammad AI", page_icon="⚡", layout="wide")

# CSS: Professional English Chat UI
st.markdown("""
    <style>
    .main { background-color: #0b141a; color: white; }
    .user-msg { background-color: #005c4b; padding: 15px; border-radius: 15px 15px 0px 15px; margin-left: auto; width: fit-content; max-width: 75%; margin-bottom: 10px; color: white; }
    .ai-msg { background-color: #202c33; padding: 15px; border-radius: 15px 15px 15px 0px; margin-right: auto; width: fit-content; max-width: 75%; margin-bottom: 10px; color: white; border: 1px solid #333; }
    .stChatInput { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI Brain Setup ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    model_id = "llama-3.3-70b-versatile"
except Exception as e:
    st.error("Error: Please check your GROQ_API_KEY in Streamlit Secrets.")

# Personality: Pure English Professional
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Sammad AI, a highly advanced artificial intelligence. You must communicate ONLY in English. Provide detailed, professional, and helpful responses to Sammad. Support all 70+ languages if requested for translation, but your primary interaction language is English."}
    ]

# --- 3. English Voice Engine ---
def get_voice_engine(text):
    try:
        # Changed to English (en)
        tts = gTTS(text=text[:400], lang='en')
        tts.save("audio_reply.mp3")
        with open("audio_reply.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay style="height:35px;"></audio>'
    except:
        return ""

# --- 4. Sidebar (All English) ---
with st.sidebar:
    st.title("⚡ Sammad AI Pro")
    st.markdown("---")
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()
    st.info("Status: Online | Engine: Llama 3.3 70B")

# --- 5. Main Chat Interface ---
st.title("Sammad AI")
st.caption("Advanced AI Interface for Professional Use")

# Display History
for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# User Input (English Placeholder)
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-msg">{prompt}</div>', unsafe_allow_html=True)

    try:
        # Get AI Response
        completion = client.chat.completions.create(
            messages=st.session_state.messages,
            model=model_id,
        )
        ai_response = completion.choices[0].message.content
        
        # UI Output
        st.markdown(f'<div class="ai-msg">{ai_response}</div>', unsafe_allow_html=True)
        
        # Professional Clipboard Box
        st.code(ai_response, language=None)
        
        # Audio Player (English Voice)
        st.markdown(get_voice_engine(ai_response), unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
    except Exception as e:
        st.error(f"System Error: {e}")
