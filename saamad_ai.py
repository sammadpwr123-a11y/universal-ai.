import streamlit as st
from groq import Groq
import os

# --- 1. Llama 3.1 Setup (Using Secrets) ---
try:
    # Ab key safe hai, code mein nazar nahi aayegi
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
model_id = "llama-3.1-8b-instant"
except Exception as e:
    st.error("Secrets mein API Key nahi mili! Settings check karein.")

# --- 2. Permanent Memory ---
chat_file = "sammad_dream_memory.txt"

def save_chat(u, a):
    with open(chat_file, "a", encoding="utf-8") as f:
        f.write(f"USER: {u}\nAI: {a}\n" + "—"*20 + "\n")

def load_chat():
    if os.path.exists(chat_file):
        with open(chat_file, "r", encoding="utf-8") as f:
            return f.read()
    return "Memory is fresh."

# --- 3. UI ---
st.set_page_config(page_title="Sammad AI Pro", layout="wide")
st.title("⚡ Sammad's Secure Llama 3.1 Server")

with st.sidebar:
    st.title("📜 Chat Logs")
    if st.button("Clear Memory"):
        if os.path.exists(chat_file): os.remove(chat_file); st.rerun()
    st.text_area("All-Time History:", load_chat(), height=500)

# --- 4. Chat + Clipboard ---
user_input = st.chat_input("Hukum karein, Sammad bhai...")

if user_input:
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_input}],
            model=model_id,
        )
        ai_res = chat_completion.choices[0].message.content
        
        save_chat(user_input, ai_res)
        
        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**Llama 3.1:** {ai_res}")
        
        # Clipboard feature
        st.copy_to_clipboard(ai_res)
        st.success("Jawab copy ho gaya!")
        
    except Exception as e:
        st.error(f"Error: {e}")
