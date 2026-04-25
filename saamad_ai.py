import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
import os

# --- 1. Page Config ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. Final Clean CSS (No Red Labels, No User Tags) ---
st.markdown("""
<style>
    .main { background-color: #131314; color: #e3e3e3; }
    
    /* Hide Streamlit User/Assistant Labels Completely */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; }

    /* User Message Bubble (Right Side) */
    [data-testid="stChatMessage-user"] { 
        flex-direction: row-reverse; 
        text-align: right; 
    }
    [data-testid="stChatMessage-user"] .stMarkdown { 
        background-color: #2b2d2f; 
        color: white; 
        padding: 10px 15px; 
        border-radius: 18px 18px 0px 18px; 
        display: inline-block;
    }

    /* Assistant Message (Left Side) */
    [data-testid="stChatMessage-assistant"] .stMarkdown { 
        background-color: transparent; 
        color: #e3e3e3; 
        padding: 10px 0; 
        display: inline-block;
    }

    /* Mic Widget Position (Left of Input) */
    .stAudioInput { width: 40px !important; margin-bottom: -62px !important; z-index: 100; position: relative; }
    .stChatInput { border-radius: 25px; background-color: #1e1f20; border: 1px solid #444746; }
</style>
""", unsafe_allow_html=True)

# --- 3. Astro Brain (Global Language + Math Expert) ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """You are Astro. 
        1. Language: Default is Roman Urdu/Hindi, but you support ALL world languages (70+). 
        2. Math: You are a calculation expert. Solve complex math instantly and accurately.
        3. Style: Friendly, professional, no 'User/AI' labels.
        4. Logic: Switch language automatically based on user's input."""}
    ]

# --- 4. Sidebar ---
with st.sidebar:
    st.title("Astro ✨")
    st.file_uploader("🖼️ Add Photo", type=['png', 'jpg', 'jpeg'])
    if st.button("Clear Memory", use_container_width=True):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()

# --- 5. Main Chat Display ---
st.markdown("<h2 style='text-align: center;'>Astro</h2>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 6. Input Section ---
mic_col, input_col = st.columns([0.06, 0.94])
with mic_col:
    recorded_voice = st.audio_input("") 

with input_col:
    user_in = st.chat_input("Ask Astro anything...")

# Logic
final_query = user_in if user_in else ("Voice command" if recorded_voice else None)

if final_query:
    st.session_state.messages.append({"role": "user", "content": final_query})
    with st.chat_message("user"):
        st.write(final_query)

    try:
        # Using Llama 3.3 70B for lightning speed
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.3 # Low temp for high math accuracy
        )
        reply = chat_completion.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.write(reply)
            
            # Action Row (Speaker Left, Copy Right)
            c1, c2 = st.columns([0.1, 0.9])
            with c1:
                if st.button("🔊"):
                    tts = gTTS(text=reply[:400], lang='hi')
                    tts.save("astro.mp3")
                    with open("astro.mp3", "rb") as f:
                        data = f.read()
                    os.remove("astro.mp3")
                    b64 = base64.b64encode(data).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay hidden></audio>', unsafe_allow_html=True)
            with c2:
                with st.expander("📋 Copy"):
                    st.code(reply, language=None)

        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"Astro Error: {e}")
