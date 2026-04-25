import streamlit as st
from groq import Groq
import os

# --- 1. Page Config (Professional Look) ---
st.set_page_config(page_title="Sukkur's First AI", page_icon="🤖", layout="wide")

# Custom CSS for Professional Dark Theme
st.markdown("""
    <style>
    .main { background-color: #131314; color: #e3e3e3; }
    .stTextInput > div > div > input { background-color: #1e1f20; color: white; border-radius: 20px; }
    .stChatMessage { background-color: #1e1f20; border-radius: 15px; padding: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Setup AI Engine ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    model_id = "llama-3.1-8b-instant"
except Exception as e:
    st.error("API Key missing! Check Streamlit Secrets.")

# --- 3. Chat State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. Sidebar (Clean History) ---
with st.sidebar:
    st.title("🤖 Sukkur's First AI")
    if st.button("+ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.caption("Recent History")
    for i, msg in enumerate(st.session_state.messages[-5:]):
        if msg["role"] == "user":
            st.markdown(f"📄 {msg['content'][:20]}...")

# --- 5. Main Chat Area ---
st.title("Sukkur's First AI")
st.caption("Advanced Artificial Intelligence at your service")

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Box (Modified Placeholder)
if prompt := st.chat_input("Ask for anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Generate AI Response
        response = client.chat.completions.create(
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            model=model_id,
        )
        full_response = response.choices[0].message.content

        # Add AI message
        with st.chat_message("assistant"):
            st.markdown(full_response)
            # Professional Code Box for copying
            st.code(full_response, language=None)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(f"Error: {e}")
