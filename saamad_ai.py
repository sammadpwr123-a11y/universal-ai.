import streamlit as st
from groq import Groq
from openai import OpenAI
import uuid

# --- 1. Page Config ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. CSS: Professional Gemini Clone ---
st.markdown("""
<style>
    .main { background-color: #131314; color: #e3e3e3; }
    header { visibility: hidden; }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    
    /* Message Alignment */
    .user-bubble { background-color: #2b2d2f; color: white; padding: 12px 20px; border-radius: 20px 20px 2px 20px; float: right; clear: both; margin-bottom: 20px; max-width: 70%; }
    .astro-text { color: #e3e3e3; padding: 10px 0; float: left; clear: both; margin-bottom: 20px; max-width: 85%; font-size: 16px; }

    /* Fixed Input Bar */
    div[data-testid="stChatInput"] { 
        position: fixed; bottom: 30px; width: 60% !important; left: 20% !important;
        background-color: #1e1f20 !important; border-radius: 28px !important;
        border: 1px solid #444746 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. Chat Session Management ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "active_id" not in st.session_state:
    sid = str(uuid.uuid4())
    st.session_state.sessions[sid] = {"title": "New Chat", "msgs": []}
    st.session_state.active_id = sid

# --- 4. Sidebar: History ---
with st.sidebar:
    st.title("Astro ✨")
    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.sessions[new_id] = {"title": "New Chat", "msgs": []}
        st.session_state.active_id = new_id
        st.rerun()
    
    st.markdown("---")
    for sid in list(st.session_state.sessions.keys()):
        if st.button(f"💬 {st.session_state.sessions[sid]['title'][:15]}...", key=sid):
            st.session_state.active_id = sid
            st.rerun()

# --- 5. Main UI ---
current_chat = st.session_state.sessions[st.session_state.active_id]
st.markdown("<h3 style='text-align: center; color: #8ab4f8;'>Astro</h3>", unsafe_allow_html=True)

for m in current_chat["msgs"]:
    if m["role"] == "user":
        st.markdown(f'<div class="user-bubble">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="astro-text">{m["content"]}</div>', unsafe_allow_html=True)
        if "gen_img" in m: st.image(m["gen_img"])

# --- 6. Input Section ---
c1, c2, c3 = st.columns([0.07, 0.07, 0.86])
with c1: pic = st.file_uploader("➕", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
with c2: voice = st.audio_input("🎤", label_visibility="collapsed")
with c3: u_in = st.chat_input("Ask Astro anything...")

# --- 7. Processing ---
if u_in or pic:
    prompt = u_in if u_in else "Analyzed Image"
    if current_chat["title"] == "New Chat": current_chat["title"] = prompt[:20]
    
    current_chat["msgs"].append({"role": "user", "content": prompt})

    try:
        # Check for Image Creation Command
        if any(x in prompt.lower() for x in ["create", "generate", "image", "tasveer"]):
            client_oa = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            img_res = client_oa.images.generate(model="dall-e-3", prompt=prompt, n=1)
            current_chat["msgs"].append({"role": "assistant", "content": "Ye rahi aapki tasveer!", "gen_img": img_res.data[0].url})
        else:
            # Standard Text Reply
            client_gr = Groq(api_key=st.secrets["GROQ_API_KEY"])
            res = client_gr.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Reply in Roman Urdu only. Be friendly."}] + 
                         [{"role": m["role"], "content": m["content"]} for m in current_chat["msgs"]]
            )
            current_chat["msgs"].append({"role": "assistant", "content": res.choices[0].message.content})
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}. Make sure OPENAI_API_KEY is in Secrets!")
