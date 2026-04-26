import streamlit as st
from groq import Groq
from openai import OpenAI
import uuid

# --- 1. Page Configuration ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. CSS: Fixed Overlay Logic (No more overlapping) ---
st.markdown("""
<style>
    .main { background-color: #131314; color: #e3e3e3; }
    header { visibility: hidden; }
    
    /* Hide Default Avatar/Icons */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; }

    /* Alignment Logic */
    .user-container { display: flex; justify-content: flex-end; width: 100%; margin-bottom: 25px; }
    .user-bubble { background-color: #2b2d2f; color: white; padding: 12px 20px; border-radius: 20px 20px 2px 20px; max-width: 75%; }
    
    .astro-container { display: flex; justify-content: flex-start; width: 100%; margin-bottom: 25px; }
    .astro-text { color: #e3e3e3; padding: 10px 0; max-width: 85%; font-size: 17px; line-height: 1.6; }

    /* FIXED SEARCH BAR & BUTTONS (No Overlap) */
    .fixed-footer {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 60%; z-index: 1000; display: flex; align-items: center;
        background-color: #1e1f20; border: 1px solid #444746; border-radius: 30px; padding: 5px 15px;
    }
    
    /* This targets the actual input box inside the fixed area */
    div[data-testid="stChatInput"] { border: none !important; background: transparent !important; }
    
    /* Make buttons small and round */
    .stFileUploader section { padding: 0 !important; }
    .stAudioInput button { background: transparent !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. Chat Session & History ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "active_id" not in st.session_state:
    session_id = str(uuid.uuid4())
    st.session_state.sessions[session_id] = {"title": "New Chat", "msgs": []}
    st.session_state.active_id = session_id

# --- 4. Sidebar: History ---
with st.sidebar:
    st.title("Astro ✨")
    if st.button("+ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.sessions[new_id] = {"title": "New Chat", "msgs": []}
        st.session_state.active_id = new_id
        st.rerun()
    
    st.write("---")
    for sid, sdata in list(st.session_state.sessions.items()):
        if st.button(f"💬 {sdata['title'][:20]}...", key=sid):
            st.session_state.active_id = sid
            st.rerun()

# --- 5. Main Screen ---
current_chat = st.session_state.sessions[st.session_state.active_id]
st.markdown("<h3 style='text-align: center; color: #8ab4f8; margin-top: -50px;'>Astro</h3>", unsafe_allow_html=True)

# Display Messages
for m in current_chat["msgs"]:
    if m["role"] == "user":
        st.markdown(f'<div class="user-container"><div class="user-bubble">{m["content"]}</div></div>', unsafe_allow_html=True)
        if "img" in m: st.image(m["img"], width=300)
    else:
        st.markdown(f'<div class="astro-container"><div class="astro-text">{m["content"]}</div></div>', unsafe_allow_html=True)
        if "gen_img" in m: st.image(m["gen_img"], width=450)

# --- 6. Input Section (Simplified to prevent Button Error) ---
# Maine columns ko adjust kiya hai taake ye mobile/web dono par overlap na ho
st.write("---")
c1, c2, c3 = st.columns([0.08, 0.08, 0.84])
with c1:
    pasted_img = st.file_uploader("➕", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
with c2:
    voice_msg = st.audio_input("🎤", label_visibility="collapsed")
with c3:
    u_in = st.chat_input("Ask Astro anything...")

# --- 7. Processing ---
if u_in or pasted_img:
    prompt = u_in if u_in else "Uploaded a picture"
    if current_chat["title"] == "New Chat":
        current_chat["title"] = prompt[:25]
    
    # Save User Msg
    msg_entry = {"role": "user", "content": prompt}
    if pasted_img: msg_entry["img"] = pasted_img
    current_chat["msgs"].append(msg_entry)

    try:
        # Check if user wants an image (e.g., "create", "generate")
        if any(word in prompt.lower() for word in ["create", "generate", "image", "banao"]):
            oa_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            img_gen = oa_client.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
            current_chat["msgs"].append({"role": "assistant", "content": "Ye rahi aapki image:", "gen_img": img_gen.data[0].url})
        else:
            # Text Response
            gr_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            res = gr_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "You are Astro. Reply in Roman Urdu. End with a friendly question."}] + 
                         [{"role": m["role"], "content": m["content"]} for m in current_chat["msgs"]]
            )
            current_chat["msgs"].append({"role": "assistant", "content": res.choices[0].message.content})
        
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")
