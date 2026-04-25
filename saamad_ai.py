import streamlit as st
from groq import Groq
from gtts import gTTS
import base64

# --- 1. Page Config (Naam Change: Sammad AI) ---
st.set_page_config(page_title="Sammad AI", page_icon="⚡", layout="wide")

# CSS: Message Alignment (User: Right, AI: Left)
st.markdown("""
    <style>
    .main { background-color: #0b141a; color: white; }
    .user-msg { background-color: #005c4b; padding: 15px; border-radius: 15px 15px 0px 15px; margin-left: auto; width: fit-content; max-width: 75%; margin-bottom: 10px; color: white; }
    .ai-msg { background-color: #202c33; padding: 15px; border-radius: 15px 15px 15px 0px; margin-right: auto; width: fit-content; max-width: 75%; margin-bottom: 10px; color: white; border: 1px solid #333; }
    .stChatInput { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Brain Setup ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    model_id = "llama-3.3-70b-versatile"
except Exception as e:
    st.error("Bhai, Secrets mein API Key dalo pehle!")

# Personality: No "Hukum", Only Dosti
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Sammad AI. Talk to Sammad like a close friend in Roman Urdu/Hindi. Don't be formal, don't say 'Hukum' or 'Sir'. Be cool, smart, and use 70+ languages if asked. By default, speak Roman Urdu."}
    ]

# --- 3. Voice Player ---
def get_voice(text):
    try:
        tts = gTTS(text=text[:350], lang='hi')
        tts.save("reply.mp3")
        with open("reply.mp3", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        return f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay style="height:35px;"></audio>'
    except: return ""

# --- 4. Sidebar ---
with st.sidebar:
    st.title("⚡ Sammad AI")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()
    st.info("Bhai, ab ye tere style mein baat karega!")

# --- 5. Main Chat ---
st.title("Sammad AI")

# Display History
for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    st.markdown(f'<div class="{role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# User Input (Placeholder change)
if prompt := st.chat_input("Haan bhai, bolo kya baat hai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-msg">{prompt}</div>', unsafe_allow_html=True)

    try:
        # Response generation
        completion = client.chat.completions.create(
            messages=st.session_state.messages,
            model=model_id,
        )
        ai_ans = completion.choices[0].message.content
        
        # UI Display
        st.markdown(f'<div class="ai-msg">{ai_ans}</div>', unsafe_allow_html=True)
        
        # Clipboard Support
        st.code(ai_ans, language=None)
        
        # Audio
        st.markdown(get_voice(ai_ans), unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "assistant", "content": ai_ans})
    except Exception as e:
        st.error(f"Error: {e}")
