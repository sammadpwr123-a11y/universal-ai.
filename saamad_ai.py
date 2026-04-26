import streamlit as st
from groq import Groq
from openai import OpenAI
import uuid

# --- 1. Page Configuration ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. CSS for Layout & Buttons (No more messy icons) ---
st.markdown("""
<style>
    .main { background-color: #131314; color: #e3e3e3; }
    header { visibility: hidden; }
    
    /* Message Alignment */
    .user-msg { background-color: #2b2d2f; color: white; padding: 12px 20px; border-radius: 20px 20px 2px 20px; float: right; clear: both; margin-bottom: 15px; max-width: 70%; }
    .astro-msg { color: #e3e3e3; padding: 10px 0; float: left; clear: both; margin-bottom: 15px; max-width: 85%; font-size: 16px; }

    /* Fixed Bottom Control Bar */
    .stChatInput { position: fixed; bottom: 30px; width: 50% !important; left: 25% !important; z-index: 1000; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #1e1f20 !important; width: 260px !important; }
    .stButton>button { background-color: #333; color: white; border-radius: 10px; width: 100%; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 3. Chat Session State ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "active_id" not in st.session_state:
    session_id = str(uuid.uuid4())
    st.session_state.sessions[session_id] = {"title": "New Chat", "msgs": []}
    st.session_state.active_id = session_id

# --- 4. Sidebar (Save Chat Logic) ---
with st.sidebar:
    st.markdown("### Astro ✨")
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.sessions[new_id] = {"title": "New Chat", "msgs": []}
        st.session_state.active_id = new_id
        st.rerun()
    
    st.write("---")
    st.write("Recent Chats")
    for sid in list(st.session_state.sessions.keys()):
        title = st.session_state.sessions[sid]["title"]
        if st.button(f"💬 {title[:15]}...", key=sid):
            st.session_state.active_id = sid
            st.rerun()

# --- 5. Main Chat UI ---
current_chat = st.session_state.sessions[st.session_state.active_id]
st.markdown("<h2 style='text-align: center; color: #8ab4f8; margin-top: -50px;'>Astro</h2>", unsafe_allow_html=True)

# Container for messages
chat_placeholder = st.container()
with chat_placeholder:
    for m in current_chat["msgs"]:
        if m["role"] == "user":
            st.markdown(f'<div class="user-msg">{m["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="astro-msg">{m["content"]}</div>', unsafe_allow_html=True)
            if "img_url" in m:
                st.image(m["img_url"], caption="Generated Image")

# --- 6. Fixed Inputs (Plus, Mic, Text) ---
# Hum columns use karenge taake cheezein ek line mein rahein
input_col_1, input_col_2, input_col_3 = st.columns([0.06, 0.06, 0.88])

with input_col_1:
    pasted_img = st.file_uploader("➕", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
with input_col_2:
    voice_data = st.audio_input("🎤", label_visibility="collapsed")
with input_col_3:
    user_input = st.chat_input("Ask Astro anything...")

# --- 7. Logic (AI Response & Image Generation) ---
if user_input or pasted_img:
    prompt = user_input if user_input else "Uploaded an image"
    
    # Update sidebar title
    if current_chat["title"] == "New Chat":
        current_chat["title"] = prompt[:20]

    current_chat["msgs"].append({"role": "user", "content": prompt})

    try:
        # Check if user wants to create an image
        if any(x in prompt.lower() for x in ["create", "generate", "image", "banao", "tasveer"]):
            client_oa = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client_oa.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
            current_chat["msgs"].append({"role": "assistant", "content": "Ye rahi aapki tasveer!", "img_url": response.data[0].url})
        else:
            # Standard Text Response
            client_gr = Groq(api_key=st.secrets["GROQ_API_KEY"])
            chat_completion = client_gr.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Reply in Roman Urdu. Be helpful."}] + 
                         [{"role": m["role"], "content": m["content"]} for m in current_chat["msgs"]]
            )
            current_chat["msgs"].append({"role": "assistant", "content": chat_completion.choices[0].message.content})
        
        st.rerun()
    except Exception as e:
        st.error(f"Something went wrong: {e}")
