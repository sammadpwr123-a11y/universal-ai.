import streamlit as st
from groq import Groq
import uuid

# --- 1. Page Configuration ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. CSS: Clean Gemini UI with No Overlap ---
st.markdown("""
<style>
    .main { background-color: #131314; color: #e3e3e3; padding-bottom: 100px; }
    [data-testid="stSidebar"] { background-color: #1e1f20; border-right: 1px solid #333; }
    
    /* Message Alignment */
    .user-msg { 
        float: right; clear: both; background-color: #2b2d2f; 
        color: white; padding: 12px 18px; border-radius: 18px 18px 2px 18px; 
        margin-bottom: 15px; max-width: 75%; 
    }
    .astro-msg { 
        float: left; clear: both; background-color: transparent; 
        color: #e3e3e3; padding: 10px 0; margin-bottom: 20px; 
        max-width: 85%; font-size: 16px; line-height: 1.6;
    }

    /* Fixed Bottom Bar Logic (Gemini Style) */
    .stChatInputContainer {
        padding-bottom: 20px;
        background-color: #131314 !important;
    }
    
    /* Mic and Upload Button Styling */
    button[kind="secondary"] {
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Session State Management ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "active_id" not in st.session_state:
    uid = str(uuid.uuid4())
    st.session_state.sessions[uid] = {"title": "New Chat", "msgs": []}
    st.session_state.active_id = uid

# --- 4. Sidebar: History & Menu ---
with st.sidebar:
    st.title("Astro ✨")
    if st.button("➕ New Chat", use_container_width=True):
        new_uid = str(uuid.uuid4())
        st.session_state.sessions[new_uid] = {"title": "New Chat", "msgs": []}
        st.session_state.active_id = new_uid
        st.rerun()
    
    st.write("---")
    for s_id, s_data in list(st.session_state.sessions.items()):
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            if st.button(f"💬 {s_data['title'][:20]}", key=f"s_{s_id}"):
                st.session_state.active_id = s_id
                st.rerun()
        with col2:
            if st.button("⋮", key=f"m_{s_id}"):
                pass # Menu logic can be added here

# --- 5. Main Chat Area ---
active_session = st.session_state.sessions[st.session_state.active_id]

st.markdown("<h3 style='text-align: center; opacity: 0.5;'>Astro</h3>", unsafe_allow_html=True)

# Container for messages to prevent layout breaking
for m in active_session["msgs"]:
    if m["role"] == "user":
        st.markdown(f'<div class="user-msg">{m["content"]}</div>', unsafe_allow_html=True)
        if "img" in m and m["img"]:
            st.image(m["img"], width=300)
    else:
        st.markdown(f'<div class="astro-msg">{m["content"]}</div>', unsafe_allow_html=True)

# --- 6. The "Gemini" Input Bar (Functional) ---
# Paste Screenshot Feature: st.file_uploader handles Ctrl+V in modern browsers automatically
with st.container():
    col_mic, col_add, col_txt = st.columns([0.05, 0.05, 0.9])
    
    with col_mic:
        voice = st.audio_input("🎤", key="mic", label_visibility="collapsed")
    
    with col_add:
        # Note: file_uploader in Streamlit supports direct Ctrl+V (Paste) from clipboard
        pasted_img = st.file_uploader("➕", type=['png', 'jpg', 'jpeg'], key="paste_box", label_visibility="collapsed")
    
    with col_txt:
        user_input = st.chat_input("Ask Astro anything...")

# Processing Logic
if user_input or pasted_img or voice:
    final_input = user_input if user_input else "Uploaded Content"
    
    # Update Session Title
    if active_session["title"] == "New Chat":
        active_session["title"] = final_input[:20]
    
    # Save User Message
    msg_data = {"role": "user", "content": final_input}
    if pasted_img:
        msg_data["img"] = pasted_img
    active_session["msgs"].append(msg_data)
    
    # AI Response
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are Astro. Professional & Friendly."}] + 
                     [{"role": m["role"], "content": m["content"]} for m in active_session["msgs"]]
        )
        active_session["msgs"].append({"role": "assistant", "content": res.choices[0].message.content})
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")
