import streamlit as st
from groq import Groq
import os

# --- 1. Llama 3.1 Ultra-Power Setup ---
try:
    # Key direct code mein set kar di hai
    client = Groq(api_key="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")
    # Sabse powerful model
    model_id = "llama-3.1-70b-versatile"
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. Permanent Memory (Saalon tak save rahega) ---
chat_file = "sammad_dream_memory.txt"

def save_chat(u, a):
    with open(chat_file, "a", encoding="utf-8") as f:
        f.write(f"USER: {u}\nAI: {a}\n" + "—"*30 + "\n")

def load_chat():
    if os.path.exists(chat_file):
        with open(chat_file, "r", encoding="utf-8") as f:
            return f.read()
    return "Memory is fresh. No history yet."

# --- 3. UI Design ---
st.set_page_config(page_title="Sammad Llama 3.1 Pro", layout="wide")
st.title("⚡ Sammad's Ultra-Level Llama 3.1 Server")
st.markdown("### 5 Years Wait Over - Dream Tool Active 🚀")

# --- 4. Sidebar (Permanent Records) ---
with st.sidebar:
    st.title("📜 Permanent Memory")
    if st.button("Clear Memory"):
        if os.path.exists(chat_file): os.remove(chat_file); st.rerun()
    st.text_area("All-Time Records:", load_chat(), height=600)

# --- 5. Chat Engine ---
user_input = st.chat_input("Ask Llama 3.1 anything...")

if user_input:
    try:
        # Llama 3.1 70B Response
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_input}],
            model=model_id,
        )
        ai_res = chat_completion.choices[0].message.content
        
        # Save & Display
        save_chat(user_input, ai_res)
        st.info(f"**Sammad:** {user_input}")
        st.success(f"**Llama 3.1:** {ai_res}")
        
        st.rerun()
    except Exception as e:
        st.error(f"System Error: {e}")
