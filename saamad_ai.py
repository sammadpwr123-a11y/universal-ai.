import streamlit as st
from groq import Groq
from gtts import gTTS
import base64
import os

# --- 1. Page Configuration (Title and Icon like Gemini) ---
st.set_page_config(page_title="Astro AI", page_icon="✨", layout="wide")

# --- 2. Hoo-boo-Hoo Gemini Duplicate CSS (Dark Mode & Layout) ---
st.markdown("""
<style>
    /* Pure Gemini Dark Theme */
    :root { font-family: 'Google Sans', Arial, sans-serif; }
    .main { background-color: #131314; color: #e3e3e3; padding-bottom: 80px; } /* Space for fixed footer */
    
    /* Fixed Input Area at Bottom (Hoo-boo-Hoo duplicate) */
    div[data-testid="stChatInput"] { position: fixed; bottom: 0; left: 0; right: 0; padding: 10px 5% 20px 5%; background-color: #131314; z-index: 999; border-top: 1px solid #333; }
    .stChatInput { border-radius: 30px; background-color: #1e1f20; border: 1px solid #444746; padding: 5px 15px;}
    .stChatInput > div > div > input { background-color: transparent; color: white; font-size: 16px; }

    /* Fix Microphone styling to be inside the input area like a small icon */
    .stAudioInput { width: 40px !important; margin-left: 10px; margin-bottom: 5px; background: none !important;}
    .stAudioInput > div > button { background-color: transparent !important; color: #8ab4f8 !important; border-radius: 50%; width: 35px; height: 35px;}

    /* Gemini Message Bubbles Style (Standard look, no heavy color) */
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; padding: 15px 0;}
    [data-testid="stChatMessage"] .stMarkdown { border-radius: 12px; font-size: 16px; display: inline-block;}
    [data-testid="stChatMessage-user"] { text-align: right; }
    [data-testid="stChatMessage-user"] .stMarkdown { background-color: #005c4b; color: white; padding: 12px 18px; }
    [data-testid="stChatMessage-assistant"] { text-align: left; }
    [data-testid="stChatMessage-assistant"] .stMarkdown { background-color: transparent; color: #e3e3e3; padding: 0 10px; }

    /* Icons Row (Copy & Voice controls) below message */
    .chat-controls { display: flex; align-items: center; gap: 10px; margin-top: 10px; opacity: 0.8;}
    .control-btn { cursor: pointer; font-size: 18px; background: none; border: none; color: #e3e3e3; }
    .control-btn:hover { color: #8ab4f8; }
</style>
""", unsafe_allow_html=True)

# --- 3. Initialize Astro (Roman Urdu Master) ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Astro. Reply in Roman Urdu. Be sleek, friendly, and smart like Gemini. Only switch languages if user specifically asks."}
    ]

# --- 4. Sidebar (Replicated Gemini Panel) ---
with st.sidebar:
    st.title("Astro ✨")
    st.markdown("---")
    # FEATURE 5: + Add Photo Option
    uploaded_image = st.file_uploader("+ Add Photo", type=['png', 'jpg', 'jpeg'], help="Standard file upload for photo analysis.")
    # Gemini options
    uploaded_audio = st.file_uploader("Upload Audio command", type=['mp3', 'wav', 'm4a'])
    uploaded_doc = st.file_uploader("Upload Document", type=['pdf', 'txt'])
    
    if st.button("New Chat", use_container_width=True):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()

# --- 5. Main Chat Area ---
# No huge title, standard Gemini name centered
st.markdown("<h3 style='text-align: center; color: #8ab4f8;'>Astro</h3>", unsafe_allow_html=True)

# Display Chat History
for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- 6. Hybrid Input Area (Fixed Bottom - Text + Mic) ---
# Gemini layout puts Mic on the far left of the text bar.
# Streamlit structure requires the widgets to be placed, CSS handles position.

st.write("---") # Visual separator before fixed area starts
user_query = st.chat_input("Ask Astro anything...")

# Process Input Logic
final_input = user_query
if uploaded_image:
    final_input = final_input if final_input else "[Analyzing Attached Photo]"

if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})
    with st.chat_message("user"):
        st.write(final_input)
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Picture", width=250)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        ai_ans = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.write(ai_ans)
            
            # --- FIXED: Icons Row (Voice & Copy) ---
            st.markdown(f'''
                <div class="chat-controls">
                    <button class="control-btn" title="Copy text" onclick="alert('Raw text for copy: {base64.b64encode(ai_ans.encode()).decode()}')">📋</button>
                    <button class="control-btn" title="Synthesize Voice" onclick="document.getElementById('play_btn').click()">🎙️</button>
                </div>
            ''', unsafe_allow_html=True)
            
            # Hidden voice processing (Synthesize voice on user demand)
            col_l, col_r = st.columns([0.1, 0.9])
            with col_l:
                if st.button("🔊 Play Voice", key="play_btn_trigger"):
                    tts = gTTS(text=ai_ans[:350], lang='hi') # hindi tone for Roman Urdu
                    tts.save("reply.mp3")
                    with open("reply.mp3", "rb") as f:
                        data = f.read()
                    os.remove("reply.mp3")
                    b64 = base64.b64encode(data).decode()
                    st.markdown(f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay style="height:35px;"></audio>', unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": ai_ans})
        
    except Exception as e:
        st.error(f"Error: {e}")
