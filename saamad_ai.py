import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
import os

# --- 1. Page Setup ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. THE "ZERO GALTI" CSS ---
st.markdown("""
<style>
    /* Gemini Background */
    .main { background-color: #131314; color: #e3e3e3; }

    /* Remove ALL default Streamlit headers, avatars, and labels */
    header, [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"], .st-emotion-cache-jt7003 {
        display: none !important;
    }

    /* RIGHT/LEFT ALIGNMENT LOGIC */
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; margin-bottom: 5px !important; padding: 0 !important; }
    
    /* User Message Style (Extreme Right) */
    [data-testid="stChatMessage-user"] { display: flex; justify-content: flex-end; }
    [data-testid="stChatMessage-user"] div[data-testid="stMarkdownContainer"] {
        background-color: #2b2d2f; color: white; padding: 12px 18px; border-radius: 22px 22px 4px 22px; max-width: 75%;
    }

    /* Assistant Message Style (Extreme Left) */
    [data-testid="stChatMessage-assistant"] { display: flex; justify-content: flex-start; }
    [data-testid="stChatMessage-assistant"] div[data-testid="stMarkdownContainer"] {
        background-color: transparent; color: #e3e3e3; padding: 12px 0; max-width: 85%;
    }

    /* SLEEK SEARCH BAR (Fixed at Bottom, Chota and Patla) */
    div[data-testid="stChatInput"] { 
        position: fixed; bottom: 30px; width: 60% !important; left: 20% !important;
        background-color: #1e1f20 !important; border-radius: 30px !important;
        border: 1px solid #444746 !important; height: 50px !important;
    }
    
    /* Tiny Icons Styling */
    .tiny-btn { 
        background: none; border: none; color: #8e918f; cursor: pointer; 
        font-size: 16px; margin-right: 10px; 
    }
    .tiny-btn:hover { color: white; }

    /* Fix Mic Widget */
    .stAudioInput { width: 45px !important; position: fixed; bottom: 32px; left: 16%; z-index: 9999; }
</style>
""", unsafe_allow_html=True)

# --- 3. Astro Logic ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Astro. 1. Reply in the same language user uses (English, Roman Urdu, etc.). 2. Always end with a short, friendly follow-up question related to the topic. 3. No labels or icons in text."}
    ]

# --- 4. Sidebar ---
with st.sidebar:
    st.title("Astro ✨")
    st.file_uploader("+ Add Photo", type=['png', 'jpg', 'jpeg'])
    if st.button("Delete Chat History"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()

# --- 5. Main Chat ---
st.markdown("<h2 style='text-align: center; color: #8ab4f8;'>Astro</h2>", unsafe_allow_html=True)

# Container for messages to prevent scrolling issues
for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 6. Input Area ---
# Mic is fixed via CSS at bottom-left
voice_in = st.audio_input("") 
user_in = st.chat_input("Hukum karein...")

if user_in:
    st.session_state.messages.append({"role": "user", "content": user_in})
    with st.chat_message("user"):
        st.write(user_in)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.6
        )
        ans = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.write(ans)
            
            # --- TINY ICONS ROW ---
            icon_col1, icon_col2, _ = st.columns([0.05, 0.05, 0.9])
            with icon_col1:
                if st.button("🔊", key=f"v_{len(st.session_state.messages)}"):
                    tts = gTTS(text=ans[:300], lang='hi')
                    tts.save("reply.mp3")
                    with open("reply.mp3", "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" autoplay hidden></audio>', unsafe_allow_html=True)
            with icon_col2:
                # Chota Clipboard Expand
                with st.popover("📋"):
                    st.code(ans, language=None)

        st.session_state.messages.append({"role": "assistant", "content": ans})
        st.rerun() # Refresh to clear input and fix layout
        
    except Exception as e:
        st.error(f"Error: {e}")
