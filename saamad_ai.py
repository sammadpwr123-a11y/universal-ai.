import streamlit as st
from groq import Groq
import uuid

# --- 1. Page Config ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. CSS: Custom Gemini UI ---
st.markdown("""
<style>
    .main { background-color: #131314; color: #e3e3e3; }
    [data-testid="stSidebar"] { background-color: #1e1f20; }
    
    /* Hide Default Streamlit Elements */
    header, [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    
    /* Message Container */
    .chat-wrapper { display: flex; flex-direction: column; width: 100%; padding: 10px; }
    
    /* User: Extreme Right */
    .user-box { align-self: flex-end; background-color: #2b2d2f; color: white; padding: 12px 18px; border-radius: 20px 20px 4px 20px; max-width: 70%; margin-bottom: 15px; text-align: left; }
    
    /* Astro: Extreme Left */
    .astro-box { align-self: flex-start; background-color: transparent; color: #e3e3e3; padding: 10px 0; max-width: 85%; margin-bottom: 20px; font-size: 17px; line-height: 1.6; }

    /* Search Bar Fixed at Bottom */
    div[data-testid="stChatInput"] { position: fixed; bottom: 30px; width: 60% !important; left: 20% !important; background-color: #1e1f20 !important; border-radius: 30px !important; border: 1px solid #444746 !important; }

    /* Tiny Control Buttons */
    .control-btn { background: none; border: none; color: #8e918f; cursor: pointer; font-size: 14px; margin-right: 8px; }
</style>
""", unsafe_allow_html=True)

# --- 3. Persistent History Engine ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} # Storage for multiple chat sessions
if "current_id" not in st.session_state:
    # Creating the very first chat
    first_id = str(uuid.uuid4())
    st.session_state.current_id = first_id
    st.session_state.all_chats[first_id] = {"title": "New Chat", "messages": []}

# --- 4. Sidebar: Gemini Navigation ---
with st.sidebar:
    st.title("Astro ✨")
    # NEW CHAT BUTTON (Requirement from screenshot 2)
    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.all_chats[new_id] = {"title": "New Chat", "messages": []}
        st.session_state.current_id = new_id
        st.rerun()

    st.markdown("---")
    st.subheader("Recent Chats")
    # Display saved chats
    for chat_id, data in st.session_state.all_chats.items():
        if st.button(f"💬 {data['title']}", key=chat_id):
            st.session_state.current_id = chat_id
            st.rerun()

# --- 5. Main Chat Area ---
active_chat = st.session_state.all_chats[st.session_state.current_id]
st.markdown("<h3 style='text-align: center; color: #8ab4f8;'>Astro</h3>", unsafe_allow_html=True)

# Display Messages using Custom CSS
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
for msg in active_chat["messages"]:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-box">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="astro-box">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. Input Logic ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
user_query = st.chat_input("Ask Astro anything...") # English fix from screenshot 1

if user_query:
    # First message becomes the chat title in sidebar
    if not active_chat["messages"]:
        active_chat["title"] = user_query[:25]
        
    active_chat["messages"].append({"role": "user", "content": user_query})
    
    try:
        # Instruction for Roman Urdu + Follow up
        system_prompt = {"role": "system", "content": "You are Astro. Reply in Roman Urdu/Hindi. Give detailed answers. Always end with a friendly follow-up question."}
        history = [system_prompt] + active_chat["messages"]
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=history,
            temperature=0.7
        )
        ans = completion.choices[0].message.content
        active_chat["messages"].append({"role": "assistant", "content": ans})
        st.rerun()
        
    except Exception as e:
        st.error(f"Astro Error: {e}")
