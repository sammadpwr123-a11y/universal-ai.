import streamlit as st
from groq import Groq
import os

# --- 1. Page Config ---
st.set_page_config(page_title="Sukkur's First AI", page_icon="⚡", layout="wide")

# --- 2. Advanced CSS (For Right/Left Chat Bubbles) ---
st.markdown("""
    <style>
    .main { background-color: #0f1116; color: #ffffff; }
    /* User Message - Right Side */
    .user-bubble {
        background-color: #005c4b;
        padding: 15px;
        border-radius: 15px 15px 0px 15px;
        margin-bottom: 20px;
        width: fit-content;
        max-width: 70%;
        margin-left: auto;
        color: white;
    }
    /* AI Message - Left Side */
    .ai-bubble {
        background-color: #202c33;
        padding: 15px;
        border-radius: 15px 15px 15px 0px;
        margin-bottom: 20px;
        width: fit-content;
        max-width: 70%;
        margin-right: auto;
        color: white;
    }
    .stTextInput > div > div > input { background-color: #2a3942; color: white; border-radius: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AI Engine Setup ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    model_id = "llama-3.1-8b-instant"
except Exception as e:
    st.error("API Key missing!")

if "messages" not in st.session_state:
    # Brain Injection: Setting the AI's personality
    st.session_state.messages = [
        {"role": "system", "content": "You are Sukkur's First AI. Talk to Sammad like a best friend in Roman Urdu/Hindi. Don't use difficult bookish Urdu. Be smart, funny, and direct. You support 70+ languages, if someone asks in another language, reply in that."}
    ]

# --- 4. Sidebar ---
with st.sidebar:
    st.title("⚡ Sukkur AI Pro")
    if st.button("+ New Chat", use_container_width=True):
        st.session_state.messages = st.session_state.messages[:1] # Keep system prompt
        st.rerun()
    st.markdown("---")
    st.info("Ab ye smart hai aur iska dimag Hasnain se 100x tez hai! 😂")

# --- 5. Chat Display ---
for message in st.session_state.messages:
    if message["role"] == "system": continue
    
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-bubble">{message["content"]}</div>', unsafe_allow_html=True)

# --- 6. Input Area ---
if prompt := st.chat_input("Ask for anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# Logic to get response
if st.session_state.messages[-1]["role"] == "user":
    try:
        response = client.chat.completions.create(
            messages=st.session_state.messages,
            model=model_id,
        )
        full_response = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")
