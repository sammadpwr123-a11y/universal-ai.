import streamlit as st
import google.generativeai as genai
import os

# --- 1. API Configuration ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. Permanent Storage Setup ---
chat_file = "chat_history.txt"

# Function to save chat to file
def save_to_file(user_text, ai_text):
    with open(chat_file, "a", encoding="utf-8") as f:
        f.write(f"USER: {user_text}\n")
        f.write(f"AI: {ai_text}\n")
        f.write("-" * 20 + "\n")

# Function to load chat from file
def load_history():
    if os.path.exists(chat_file):
        with open(chat_file, "r", encoding="utf-8") as f:
            return f.read()
    return "No history yet."

# --- 3. UI Setup ---
st.title("🚀 Sammad's Universal AI Server")
st.subheader("Best friend Hasnain ka dushman! 😂")

# --- 4. Sidebar (Permanent Records) ---
st.sidebar.title("📜 All-Time History")
history_data = load_history()
st.sidebar.text_area("Records Saved in Server:", history_data, height=500)

if st.sidebar.button("Clear All History"):
    if os.path.exists(chat_file):
        os.remove(chat_file)
        st.rerun()

# --- 5. Chat Interface ---
user_input = st.chat_input("Hasnain ke bare mein pucho ya kuch bhi...")

if user_input:
    try:
        response = model.generate_content(user_input)
        ai_response = response.text
        
        # Save to permanent file
        save_to_file(user_input, ai_response)
        
        # Show current chat
        st.info(f"**You:** {user_input}")
        st.success(f"**AI:** {ai_response}")
        
        # Refresh to update sidebar
        st.rerun()
    except Exception as e:
        st.error(f"AI Error: {e}")
