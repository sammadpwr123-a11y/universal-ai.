import streamlit as st
from groq import Groq
import uuid

# --- 1. Page Config ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. THE ULTIMATE CSS (Applying your Screenshot Markings) ---
st.markdown("""
<style>
    /* Dark Theme */
    .main { background-color: #131314; color: #e3e3e3; }
    [data-testid="stSidebar"] { background-color: #1e1f20; border-right: 1px solid #333; }

    /* Hide Default Elements */
    header, [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    
    /* CHAT ALIGNMENT (Right for User, Left for Astro) */
    .chat-container { display: flex; flex-direction: column; width: 100%; max-width: 900px; margin: auto; }
    
    .user-msg { 
        align-self: flex-end; background-color: #2b2d2f; color: white; 
        padding: 12px 20px; border-radius: 20px 20px 2px 20px; 
        max-width: 70%; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .astro-msg { 
        align-self: flex-start; background-color: transparent; color: #e3e3e3; 
        padding: 10px 0; max-width: 85%; margin-bottom: 30px; 
        font-size: 17px; line-height: 1.6;
    }

    /* CUSTOM INPUT BAR (Mic + Plus + Input) */
    .input-wrapper {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
        width: 60%; display: flex; align-items: center; gap: 10px;
        background-color: #1e1f20; padding: 10px 20px; border-radius: 35px;
        border: 1px solid #444746; z-index: 1000;
    }

    /* Fixing Streamlit's Input Position to match your UI */
    div[data-testid="stChatInput"] { 
        background: transparent !important; border: none !important; padding: 0 !important;
    }
    
    /* Sidebar Buttons */
    .stButton>button { 
        background-color: transparent; border: none; color: #e3e3e3; 
        text-align: left; width: 100%; padding: 10px; border-radius: 8px;
    }
    .stButton>button:hover { background-color: #2b2d2f; }
</style>
""", unsafe_allow_html=True)

# --- 3. Chat Logic & History (Sidebar Feature) ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {}
if "active_id" not in st.session_state:
    uid = str(uuid.uuid4())
    st.session_state.active_id = uid
    st.session_state.sessions[uid] = {"title": "New Chat", "msgs": []}

# --- 4. Sidebar: Save Chat & Topics ---
with st.sidebar:
    st.markdown("<h2 style='color:white;'>Astro History</h2>", unsafe_allow_html=True)
    if st.button("➕ New Chat"):
        new_uid = str(uuid.uuid4())
        st.session_state.sessions[new_uid] = {"title": "New Chat", "msgs": []}
        st.session_state.active_id = new_uid
        st.rerun()
    
    st.markdown("---")
    for s_id, s_data in st.session_state.sessions.items():
        if st.button(f"💬 {s_data['title'][:20]}...", key=s_id):
            st.session_state.active_id = s_id
            st.rerun()

# --- 5. Main Screen ---
curr_session = st.session_state.sessions[st.session_state.active_id]

st.markdown("<h1 style='text-align: center; color: #8ab4f8; font-size: 24px;'>Astro</h1>", unsafe_allow_html=True)

# Display Messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for m in curr_session["msgs"]:
    if m["role"] == "user":
        st.markdown(f'<div class="user-msg">{m["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="astro-msg">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. The Input Area (Mic + Plus from your Drawing) ---
# Bottom bar columns
c1, c2, c3 = st.columns([0.05, 0.05, 0.9])
with c1:
    st.button("🎤", help="Voice Command") # Your 'Mic' marking
with c2:
    st.button("➕", help="Add Screenshot") # Your 'Add Screenshot' marking
with c3:
    u_input = st.chat_input("Ask Astro anything...")

# Processing Response
if u_input:
    # Update title
    if curr_session["title"] == "New Chat":
        curr_session["title"] = u_input[:30]
    
    curr_session["msgs"].append({"role": "user", "content": u_input})
    
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        # Custom prompt for Roman Urdu + Friendship
        sys_p = {"role": "system", "content": "You are Astro, a friendly AI. Reply in Roman Urdu/English. End with a friendly question about the topic."}
        full_history = [sys_p] + curr_session["msgs"]
        
        res = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=full_history)
        bot_res = res.choices[0].message.content
        
        curr_session["msgs"].append({"role": "assistant", "content": bot_res})
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")
