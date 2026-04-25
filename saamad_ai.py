import streamlit as st
from groq import Groq
import uuid

# --- 1. Page Configuration ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. THE FINAL MASTER CSS ---
st.markdown("""
<style>
    .main { background-color: #131314; color: #e3e3e3; }
    [data-testid="stSidebar"] { background-color: #1e1f20; border-right: 1px solid #333; width: 300px !important; }

    /* Alignment Fix */
    .user-msg { align-self: flex-end; background-color: #2b2d2f; color: white; padding: 12px 20px; border-radius: 20px 20px 2px 20px; max-width: 70%; margin-bottom: 20px; float: right; clear: both; }
    .astro-msg { align-self: flex-start; background-color: transparent; color: #e3e3e3; padding: 10px 0; max-width: 85%; margin-bottom: 30px; float: left; clear: both; font-size: 17px; }

    /* Fixed Gemini Bar at Bottom */
    .footer-container { position: fixed; bottom: 0; width: 100%; background-color: #131314; padding: 20px 0; z-index: 100; }
    
    /* Sidebar Chat Row with 3 Dots */
    .chat-row { display: flex; justify-content: space-between; align-items: center; padding: 5px; border-radius: 8px; margin-bottom: 5px; }
    .chat-row:hover { background-color: #2b2d2f; }
</style>
""", unsafe_allow_html=True)

# --- 3. Functional Logic (History & Sessions) ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "active_id" not in st.session_state:
    uid = str(uuid.uuid4())
    st.session_state.sessions[uid] = {"title": "New Chat", "msgs": []}
    st.session_state.active_id = uid

# --- 4. Sidebar: History & Functional 3 Dots ---
with st.sidebar:
    st.markdown("### Astro History")
    if st.button("➕ New Chat", use_container_width=True):
        new_uid = str(uuid.uuid4())
        st.session_state.sessions[new_uid] = {"title": "New Chat", "msgs": []}
        st.session_state.active_id = new_uid
        st.rerun()
    
    st.markdown("---")
    for s_id in list(st.session_state.sessions.keys()):
        s_data = st.session_state.sessions[s_id]
        col_title, col_menu = st.columns([0.8, 0.2])
        with col_title:
            if st.button(f"💬 {s_data['title'][:18]}", key=f"btn_{s_id}"):
                st.session_state.active_id = s_id
                st.rerun()
        with col_menu:
            # The 3 Dots Functionality
            with st.popover("⋮"):
                if st.button("🗑️ Delete", key=f"del_{s_id}"):
                    del st.session_state.sessions[s_id]
                    if st.session_state.active_id == s_id:
                        st.session_state.active_id = list(st.session_state.sessions.keys())[0] if st.session_state.sessions else None
                    st.rerun()

# --- 5. Main Screen ---
if st.session_state.active_id:
    curr_session = st.session_state.sessions[st.session_state.active_id]
    st.markdown("<h2 style='text-align: center; color: #8ab4f8;'>Astro</h2>", unsafe_allow_html=True)

    # Messages Display
    for m in curr_session["msgs"]:
        role_class = "user-msg" if m["role"] == "user" else "astro-msg"
        st.markdown(f'<div class="{role_class}">{m["content"]}</div>', unsafe_allow_html=True)
        if "img" in m: st.image(m["img"], width=300)

    # --- 6. WORKING INPUT BAR (Mic + Plus + Text) ---
    st.markdown("<div style='margin-top: 150px;'></div>", unsafe_allow_html=True) # Spacer
    
    # Input Logic with functional buttons
    with st.container():
        c1, c2, c3 = st.columns([0.07, 0.07, 0.86])
        with c1:
            # WORKING Mic
            voice_data = st.audio_input("🎤", key="mic_btn")
        with c2:
            # WORKING Screenshot/Plus
            img_file = st.file_uploader("➕", type=['png', 'jpg', 'jpeg'], key="img_btn", label_visibility="collapsed")
        with c3:
            u_input = st.chat_input("Ask Astro anything...")

    if u_input or voice_data:
        prompt = u_input if u_input else "Voice Command"
        if curr_session["title"] == "New Chat":
            curr_session["title"] = prompt[:20]
        
        # Save User Message
        user_msg = {"role": "user", "content": prompt}
        if img_file: user_msg["img"] = img_file
        curr_session["msgs"].append(user_msg)
        
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            sys_prompt = {"role": "system", "content": "You are Astro. Reply in Roman Urdu. End with a friendly question."}
            res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[sys_prompt] + curr_session["msgs"])
            curr_session["msgs"].append({"role": "assistant", "content": res.choices[0].message.content})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
