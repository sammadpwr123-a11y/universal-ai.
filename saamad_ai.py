import streamlit as st
from groq import Groq
import uuid

# --- 1. Page Configuration ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. CSS: The "Zero Streamlit" Look ---
st.markdown("""
<style>
    /* Gemini Dark Theme */
    .main { background-color: #131314; color: #e3e3e3; }
    header, [data-testid="stSidebarNav"] { visibility: hidden; }
    
    /* Message Container Logic */
    .chat-row { display: flex; width: 100%; margin-bottom: 20px; }
    .user-row { justify-content: flex-end; }
    .astro-row { justify-content: flex-start; }

    /* Bubbles Style */
    .user-bubble { 
        background-color: #2b2d2f; color: white; padding: 12px 18px; 
        border-radius: 20px 20px 4px 20px; max-width: 70%; text-align: left;
    }
    .astro-text { 
        background-color: transparent; color: #e3e3e3; padding: 10px 0; 
        max-width: 85%; font-size: 16px; line-height: 1.6;
    }

    /* Fixed Gemini Bottom Bar */
    div[data-testid="stChatInput"] { 
        position: fixed; bottom: 25px; width: 60% !important; left: 20% !important;
        background-color: #1e1f20 !important; border-radius: 28px !important;
        border: 1px solid #444746 !important; 
    }
    
    /* Small Icons Styling */
    .icon-btn { background: none; border: none; color: #8e918f; cursor: pointer; font-size: 14px; }
    
    /* Sidebar Chat History Styling */
    .stButton>button { background-color: transparent; border: none; text-align: left; color: #e3e3e3; width: 100%; }
    .stButton>button:hover { background-color: #2b2d2f; }
</style>
""", unsafe_allow_html=True)

# --- 3. Persistent Chat History Logic (Screenshot 2 Feature) ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {} # Dictionary to store all chats
if "current_session" not in st.session_state:
    st.session_state.current_session = str(uuid.uuid4())
    st.session_state.sessions[st.session_state.current_session] = {
        "title": "New Chat",
        "messages": [{"role": "system", "content": "You are Astro. Reply in Roman Urdu/English. End with a friendly follow-up question."}]
    }

# --- 4. Sidebar: History & Settings ---
with st.sidebar:
    st.title("Astro ✨")
    if st.button("+ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.sessions[new_id] = {
            "title": "New Chat",
            "messages": [{"role": "system", "content": "You are Astro. Reply in Roman Urdu/English. End with a friendly follow-up question."}]
        }
        st.session_state.current_session = new_id
        st.rerun()
    
    st.markdown("### Recent Chats")
    for session_id, data in st.session_state.sessions.items():
        if st.button(f"💬 {data['title'][:25]}...", key=session_id):
            st.session_state.current_session = session_id
            st.rerun()

# --- 5. Main Chat Interface ---
curr_session = st.session_state.sessions[st.session_state.current_session]

st.markdown("<h2 style='text-align: center; color: #8ab4f8;'>Astro</h2>", unsafe_allow_html=True)

# Custom Message Display (No Streamlit default bubbles)
for msg in curr_session["messages"]:
    if msg["role"] == "system": continue
    
    if msg["role"] == "user":
        st.markdown(f'''<div class="chat-row user-row"><div class="user-bubble">{msg["content"]}</div></div>''', unsafe_allow_html=True)
    else:
        st.markdown(f'''<div class="chat-row astro-row"><div class="astro-text">{msg["content"]}</div></div>''', unsafe_allow_html=True)

# --- 6. Input Section ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
user_input = st.chat_input("Ask Astro anything...") # English fix from screenshot 1

if user_input:
    # Update title if it's the first message
    if curr_session["title"] == "New Chat":
        curr_session["title"] = user_input[:30]
        
    curr_session["messages"].append({"role": "user", "content": user_input})
    st.markdown(f'''<div class="chat-row user-row"><div class="user-bubble">{user_input}</div></div>''', unsafe_allow_html=True)

    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=curr_session["messages"]
        )
        reply = chat_completion.choices[0].message.content
        
        st.markdown(f'''<div class="chat-row astro-row"><div class="astro-text">{reply}</div></div>''', unsafe_allow_html=True)
        
        # Tiny Icons Row
        col1, col2, _ = st.columns([0.05, 0.05, 0.9])
        with col1: st.button("🔊", key=f"v_{uuid.uuid4()}")
        with col2: st.button("📋", key=f"c_{uuid.uuid4()}")
            
        curr_session["messages"].append({"role": "assistant", "content": reply})
        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")
