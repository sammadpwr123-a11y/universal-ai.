import streamlit as st
import google.generativeai as genai
import os

# --- 1. API Configuration (Latest Power) ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Hum 'gemini-1.5-pro' use kar rahe hain jo sabse advance hai
    model = genai.GenerativeModel('gemini-1.5-pro') 
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. Permanent Storage Setup ---
chat_file = "permanent_history.txt"

def save_chat(u_text, a_text):
    with open(chat_file, "a", encoding="utf-8") as f:
        f.write(f"You: {u_text}\nAI: {a_text}\n" + "="*30 + "\n")

def get_history():
    if os.path.exists(chat_file):
        with open(chat_file, "r", encoding="utf-8") as f:
            return f.read()
    return "Abhi tak koi purani chat nahi hai."

# --- 3. UI Design ---
st.set_page_config(page_title="Sammad AI Pro", layout="wide")
st.title("🔥 Sammad's Super AI (Gemini 1.5 Pro)")
st.caption("Permanent Record System Activated")

# --- 4. Sidebar Records ---
with st.sidebar:
    st.title("📜 All-Time Chat Logs")
    if st.button("Clear All History"):
        if os.path.exists(chat_file):
            os.remove(chat_file)
            st.rerun()
    st.text_area("Server Memory:", get_history(), height=600)

# --- 5. Main Chat ---
user_msg = st.chat_input("Write anything (Latest Model is ready)...")

if user_msg:
    try:
        # Powerful response generation
        res = model.generate_content(user_msg)
        answer = res.text
        
        # Save to Server
        save_chat(user_msg, answer)
        
        # Display
        st.chat_message("user").write(user_msg)
        st.chat_message("assistant").write(answer)
        
        # Refresh sidebar
        st.rerun()
    except Exception as e:
        st.error(f"AI Power Error: {e}")
