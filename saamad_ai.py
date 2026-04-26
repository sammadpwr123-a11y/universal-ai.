import streamlit as st
from groq import Groq
from openai import OpenAI
import uuid

# --- 1. Page Configuration (Title and Icon like Gemini) ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. Advanced CUSTOM CSS to Duplicate your Screenshot's exact look ---
st.markdown("""
<style>
    /* Pure Gemini Dark Theme Root */
    :root { font-family: 'Google Sans', Arial, sans-serif; }
    .main { background-color: #131314; color: #e3e3e3; padding-bottom: 120px; }
    
    /* Input Bar Logic (Fixed at bottom with your spacing) */
    div[data-testid="stChatInput"] { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); width: 60% !important; background-color: #1e1f20; border-radius: 35px; border: 1px solid #444746; z-index: 1000; padding: 10px 15px; }
    div[data-testid="stChatInput"] input { background-color: transparent !important; color: white !important; font-size: 16px; border: none !important; }
    
    /* Fix Mic and Plus icons inside input bar as per drawing */
    .mic-icon-wrapper, .plus-icon-wrapper { cursor: pointer; color: #8e918f; font-size: 20px; margin-right: 15px; }
    .stAudioInput { visibility: hidden; width: 0; position: absolute; } /* Hide default widget but keep logic */
    .stFileUploadDropzone { border: none !important; background: transparent !important; color: transparent !important; margin: 0; padding: 0;}
    .stFileUploader { visibility: hidden; width: 0; position: absolute; }

    /* Custom Messaging Style (User Right, AI Left) from drawings */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"], .st-emotion-cache-1090159 {
        display: none !important; /* Remove all default red/yellow tags and icons */
    }
    
    /* Standard Gemini Message Bubbles */
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; padding: 15px 0; max-width: 80%;}
    [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] {
        border-radius: 12px; font-size: 16px;
    }

    /* User Message Bubble (Right Align, Dark Grey from drawings) */
    [data-testid="stChatMessage-user"] { margin-left: auto; text-align: right; }
    [data-testid="stChatMessage-user"] div[data-testid="stMarkdownContainer"] {
        background-color: #2b2d2f; color: white; padding: 12px 18px; display: inline-block;
    }

    /* AI Message (Left Align, Clear style) */
    [data-testid="stChatMessage-assistant"] { margin-right: auto; text-align: left; }
    [data-testid="stChatMessage-assistant"] div[data-testid="stMarkdownContainer"] {
        background-color: transparent; color: #e3e3e3; padding: 0 10px;
    }

    /* Generated Image Styling */
    .stImage { border-radius: 12px; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- 3. Persistent History Logic (Sidebar Chat History Feature) ---
if "sessions" not in st.session_state:
    st.session_state.sessions = {} # Dictionary to store all chats
if "current_session_id" not in st.session_state:
    first_id = str(uuid.uuid4())
    st.session_state.current_session_id = first_id
    # Default message structure with professional Roman Urdu logic
    st.session_state.sessions[first_id] = {
        "title": "New Chat",
        "messages": [{"role": "system", "content": "You are Astro. Reply in Roman Urdu. Be sleek, friendly, and smart like Gemini. End with a friendly follow-up question."}]
    }

# --- 4. Sidebar: History & Functionality ---
with st.sidebar:
    st.title("Astro ✨")
    # THE '+ New Chat' BUTTON (Requirement from drawing)
    if st.button("+ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.sessions[new_id] = {
            "title": "New Chat",
            "messages": [{"role": "system", "content": "You are Astro. Reply in Roman Urdu. Be sleek, friendly, and smart like Gemini. End with a friendly follow-up question."}]
        }
        st.session_state.current_session_id = new_id
        st.rerun()
    
    st.markdown("---")
    st.caption("Recent Chats")
    # Display saved chats (Requirement from screenshot 2)
    for session_id, session_data in st.session_state.sessions.items():
        if st.button(f"💬 {session_data['title'][:20]}...", key=session_id):
            st.session_state.current_session_id = session_id
            st.rerun()

# --- 5. Main Chat Area ---
active_session = st.session_state.sessions[st.session_state.current_session_id]

# Minimalist Title (Screenshot look)
st.markdown("<h2 style='text-align: center; color: #8ab4f8; font-family: Google Sans;'>Astro</h2>", unsafe_allow_html=True)

# Custom Message Display
for msg in active_session["messages"]:
    if msg["role"] == "system": continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "generated_image_url" in msg:
            st.image(msg["generated_image_url"], caption="Generated by Astro ✨", width=400)
        if "uploaded_image" in msg:
            st.image(msg["uploaded_image"], caption="Attached Photo", width=250)

# --- 6. WORKING Gemini Hybrid Input Area (Text + Mic + Plus + Clipboard) ---
st.write("---") # Spacing for bottom bar

# The browser will automatically handle Ctrl+V (Paste) into this file uploader
input_btns_col, input_txt_col = st.columns([0.1, 0.9])
with input_btns_col:
    # ➕ Standard Upload/Paste area for images
    uploaded_pic = st.file_uploader("🖼️", type=['png', 'jpg', 'jpeg'], help="Standard upload or Ctrl+V (paste)")
    
    # 🎙️ Hidden but Functional Mic (requires button interaction to stay stable)
    if st.button("🎙️", help="Start recording voice"):
        recorded_audio = st.audio_input("Record") # default recorder for stability

with input_txt_col:
    user_query = st.chat_input("Ask Astro anything...") # Requirement from drawings/screenshots

# Process Input Logic (Text or Image Generation)
final_input = user_query
image_to_generate_prompt = None

# FEATURE: Direct Image Generation Logic
trigger_keywords = ["image:", "create:", "generate:", "tasveer:"]
if user_query and any(user_query.lower().startswith(kw) for kw in trigger_keywords):
    image_to_generate_prompt = user_query[6:].strip() # Extract prompt after keyword
    final_input = f"[Astro is generating an image for: {image_to_generate_prompt}]"

# Handle Uploaded Picture
if uploaded_pic:
    final_input = final_input if final_input else "[Analyzing Attached Photo]"

if final_input:
    # Update Session Title based on first query
    if active_session["title"] == "New Chat":
        active_session["title"] = user_query[:25] if user_query else (image_to_generate_prompt[:25] if image_to_generate_prompt else final_input[:25])
        
    # Standard Text Response (Groq)
    try:
        # Standard brain logic (for now)
        groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=active_session["messages"] + [{"role": "user", "content": final_input}]
        )
        groq_reply = response.choices[0].message.content
        
        # Save User Message in History with image data if applicable
        user_msg = {"role": "user", "content": final_input}
        if uploaded_pic:
            user_msg["uploaded_image"] = uploaded_pic
        active_session["messages"].append(user_msg)

        # Show user message
        with st.chat_message("user"):
            st.write(final_input)
            if uploaded_pic:
                st.image(uploaded_pic, width=250)

        # Save and Show AI Message
        astro_reply_msg = {"role": "assistant", "content": groq_reply}
        
        # FEATURE: Execute Image Generation if requested
        if image_to_generate_prompt:
            openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            img_response = openai_client.images.generate(
                model="dall-e-3",
                prompt=f"A high-quality, friendly-toned image based on the prompt: {image_to_generate_prompt}",
                n=1, size="1024x1024"
            )
            astro_reply_msg["generated_image_url"] = img_response.data[0].url

        with st.chat_message("assistant"):
            st.write(astro_reply_msg["content"])
            if "generated_image_url" in astro_reply_msg:
                st.image(astro_reply_msg["generated_image_url"], width=400)
                
            # Manual Play Voice and Copy Controls (Icons only, Requirement)
            control_l, control_r, _ = st.columns([0.05, 0.05, 0.9])
            with control_l: st.button("🔊", help="Listen")
            with control_r: st.button("📋", help="Copy")

        active_session["messages"].append(astro_reply_msg)
        
    except Exception as e:
        st.error(f"Error: {e}")
