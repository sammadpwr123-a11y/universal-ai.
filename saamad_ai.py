import streamlit as st
from groq import Groq
import os

# --- 1. Llama Setup ---
# Hum ne try/except ko bilkul sahi format mein rakha hai
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    # Ye model 100% stable hai aur fast chalta hai
    model_id = "llama-3.1-8b-instant"
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. Memory System ---
chat_file = "dream_memory.txt"

def save_chat(u, a):
    with open(chat_file, "a", encoding="utf-8") as f:
        f.write(f"USER: {u}\nAI: {a}\n" + "—"*20 + "\n")

def load_chat():
    if os.path.exists(chat_file):
        with open(chat_file, "r", encoding="utf-8") as f:
            return f.read()
    return "Memory is fresh."

# --- 3. UI Design ---
st.set_page_config(page_title="Sammad AI Pro", layout="wide")
st.title("⚡ Sammad's Final Dream Server")

with st.sidebar:
    st.title("📜 Memory Logs")
    if st.button("Clear Logs"):
        if os.path.exists(chat_file):
            os.remove(chat_file)
            st.rerun()
    st.text_area("History:", load_chat(), height=500)

# --- 4. Chat Interface ---
user_input = st.chat_input("Hukum karein, Sammad bhai...")

if user_input:
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_input}],
            model=model_id,
        )
        ai_res = chat_completion.choices[0].message.content
        
        # Save to permanent memory
        save_chat(user_input, ai_res)
        
        # Display results
        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**AI:** {ai_res}")
        
        # Simple Clipboard Button
        st.copy_to_clipboard(ai_res)
        st.success("Copied to clipboard!")
        
    except Exception as e:
        st.error(f"Error: {e}")
