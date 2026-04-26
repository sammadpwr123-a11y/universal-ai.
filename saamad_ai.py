import streamlit as st
from groq import Groq
from openai import OpenAI
import uuid

# --- 1. Page Config (Professional English) ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. CSS: Clean Gemini Layout (Zero Clutter) ---
st.markdown("""
<style>
    .main { background-color: #131314; color: #e3e3e3; }
    [data-testid="stSidebar"] { background-color: #1e1f20; border-right: 1px solid #333; }
    
    /* Hide Default Streamlit Labels/Icons */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    header { visibility: hidden; }

    /* Right/Left Message Alignment */
    .chat-container { display: flex; flex-direction: column; gap: 20px; }
    .user-bubble { align-self: flex-end; background-color: #2b2d2f; color: white; padding: 12px 18px; border-radius: 20px 20px 2px 20px; max-width: 75%; text-align: left; }
    .astro-bubble { align-self: flex-start; background-color: transparent; color: #e3e3e3; padding: 10px 0; max-width: 85%; font-size: 16px; line-height: 1.6; }

    /* Fixed Bottom Search Bar (Small/Sleek) */
    div[data-testid="stChatInput"] { 
        position: fixed; bottom: 30px; width: 60% !important; left: 20% !important;
        background-color: #1e1f20 !important; border-radius: 30px !important;
        border: 1px solid #444746 !important; height: 50px !important;
    }

    /* Ctrl+V / Plus Button Styling */
    .stFileUploader { position: fixed; bottom: 35px; left: 15%; z-index: 1000; width: 40px; }
</style>
""", unsafe_allow_html=True)

# --- 3. Chat Sessions & Memory ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "active_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.sessions[new_id] = {"title": "New Chat", "msgs": []}
    st.session_state.active_id = new_id

# --- 4. Sidebar: Gemini History & New Chat ---
with st.sidebar:
    st.title("Astro ✨")
    if st.button("+ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.sessions[new_id] = {"title": "New Chat", "msgs": []}
        st.session_state.active_id = new_id
        st.rerun()
    
    st.markdown("---")
    for s_id, s_data in list(st.session_state.sessions.items()):
        col_t, col_d = st.columns([0.8, 0.2])
        with col_t:
            if st.button(f"💬 {s_data['title'][:20]}", key=s_id):
                st.session_state.active_id = s_id
                st.rerun()
        with col_d:
            if st.button("⋮", key=f"del_{s_id}"):
                del st.session_state.sessions[s_id]
                st.rerun()

# --- 5. Main Chat Interface ---
active_chat = st.session_state.sessions[st.session_state.active_id]
st.markdown("<h3 style='text-align: center; color: #8ab4f8;'>Astro</h3>", unsafe_allow_html=True)

# Display Messages
for m in active_chat["msgs"]:
    if m["role"] == "user":
        st.markdown(f'<div class="chat-container"><div class="user-bubble">{m["content"]}</div></div>', unsafe_allow_html=True)
        if "img" in m: st.image(m["img"], width=300)
    else:
        st.markdown(f'<div class="chat-container"><div class="astro-bubble">{m["content"]}</div></div>', unsafe_allow_html=True)
        if "gen_img" in m: st.image(m["gen_img"], caption="Created by Astro ✨")

# --- 6. Input Area (Plus/Paste + Mic + Text) ---
col_plus, col_mic, col_txt = st.columns([0.05, 0.05, 0.9])
with col_plus:
    # This uploader supports Ctrl+V (Paste) in most browsers
    pasted_file = st.file_uploader("➕", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
with col_mic:
    voice_input = st.audio_input("🎤", label_visibility="collapsed")

user_input = st.chat_input("Ask Astro anything...") # Professional English Placeholder

# --- 7. Processing Logic (Text & Image Generation) ---
if user_input or pasted_file:
    query = user_input if user_input else "Uploaded Image"
    
    # Auto-title for sidebar
    if active_chat["title"] == "New Chat":
        active_chat["title"] = query[:25]

    # Save User Msg
    new_user_msg = {"role": "user", "content": query}
    if pasted_file: new_user_msg["img"] = pasted_file
    active_chat["msgs"].append(new_user_msg)

    try:
        # Check if user wants to create an image
        if "create" in query.lower() or "generate" in query.lower() or "image" in query.lower():
            # IMAGE GENERATION (DALL-E 3)
            oa_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            img_res = oa_client.images.generate(model="dall-e-3", prompt=query, n=1, size="1024x1024")
            active_chat["msgs"].append({"role": "assistant", "content": "Ye rahi aapki image!", "gen_img": img_res.data[0].url})
        else:
            # TEXT RESPONSE (Groq)
            g_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            res = g_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "You are Astro. Reply in Roman Urdu. Be friendly and ask a follow-up question."}] + 
                         [{"role": m["role"], "content": m["content"]} for m in active_chat["msgs"]]
            )
            active_chat["msgs"].append({"role": "assistant", "content": res.choices[0].message.content})
        
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")
