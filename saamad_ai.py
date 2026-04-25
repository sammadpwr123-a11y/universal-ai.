import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
import os

# --- 1. Page Config ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. Heavy Custom CSS (Gemini Duplicate Logic) ---
st.markdown("""
<style>
    /* Dark Theme Background */
    .main { background-color: #131314; color: #e3e3e3; }
    
    /* Hide ALL default Streamlit Icons & Labels */
    [data-testid="stChatMessageAvatarUser"], 
    [data-testid="stChatMessageAvatarAssistant"],
    .st-emotion-cache-1090159 { display: none !important; }

    /* Message Bubble Alignment */
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; margin-bottom: 20px; }
    
    /* USER: Right Side Alignment */
    [data-testid="stChatMessage-user"] { 
        display: flex; justify-content: flex-end; text-align: right; 
    }
    [data-testid="stChatMessage-user"] .stMarkdown { 
        background-color: #2b2d2f; color: white; padding: 10px 15px; 
        border-radius: 18px 18px 0px 18px; max-width: 70%;
    }

    /* ASTRO: Left Side Alignment */
    [data-testid="stChatMessage-assistant"] { 
        display: flex; justify-content: flex-start; text-align: left; 
    }
    [data-testid="stChatMessage-assistant"] .stMarkdown { 
        background-color: transparent; color: #e3e3e3; padding: 10px 0; 
        max-width: 80%;
    }

    /* Sleek Input Bar at Bottom (Chota aur Patla) */
    div[data-testid="stChatInput"] { 
        position: fixed; bottom: 20px; padding: 0 15% !important; 
        background-color: transparent !important; 
    }
    .stChatInput { 
        border-radius: 30px !important; border: 1px solid #444746 !important; 
        height: 45px !important; 
    }

    /* Fixed Mic Position */
    .stAudioInput { width: 40px !important; margin-bottom: -55px !important; margin-left: 10px; z-index: 1000; }
</style>
""", unsafe_allow_html=True)

# --- 3. Astro Brain (With Follow-up Logic) ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """You are Astro. 
        1. Language: Reply in Roman Urdu by default. If user speaks English, you reply in English. Support all languages.
        2. Tone: Friendly like a best friend. 
        3. Structure: Give a detailed answer, then ALWAYS end with a friendly follow-up question related to the topic.
        4. Math: Super fast and accurate."""}
    ]

# --- 4. Sidebar ---
with st.sidebar:
    st.title("Astro ✨")
    st.file_uploader("+ Add Photo", type=['png', 'jpg', 'jpeg'])
    if st.button("Clear Chat"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()

# --- 5. Chat Display ---
st.markdown("<h2 style='text-align: center; color: #8ab4f8; font-family: Google Sans;'>Astro</h2>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 6. The Input (Mic + Text) ---
mic_col, in_col = st.columns([0.05, 0.95])
with mic_col:
    voice_in = st.audio_input("")

user_in = st.chat_input("Ask me anything...")

# Logic
query = user_in if user_in else ("User sent voice" if voice_in else None)

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.7
        )
        ans = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.write(ans)
            
            # Bottom Controls (Icon Only)
            c1, c2 = st.columns([0.1, 0.9])
            with c1:
                if st.button("🔊"):
                    tts = gTTS(text=ans[:300], lang='hi')
                    tts.save("v.mp3")
                    with open("v.mp3", "rb") as f:
                        data = f.read()
                    os.remove("v.mp3")
                    st.markdown(f'<audio src="data:audio/mp3;base64,{base64.b64encode(data).decode()}" autoplay hidden></audio>', unsafe_allow_html=True)
            with c2:
                with st.expander("📋"):
                    st.code(ans, language=None)

        st.session_state.messages.append({"role": "assistant", "content": ans})
        
    except Exception as e:
        st.error(f"Error: {e}")
