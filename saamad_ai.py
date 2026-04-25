import streamlit as st
import google.generativeai as genai
import os

# --- 1. AI CONFIGURATION ---
# Put your Google Gemini API Key here
genai.configure(api_key="google API key")
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- 2. APP PAGE SETTINGS ---
st.set_page_config(page_title="Sammad AI Server", page_icon="💻")

# --- 3. MULTI-USER SYSTEM ---
st.sidebar.title("System Settings")
user_name = st.sidebar.text_input("Enter Your Name:", "Guest").strip().lower()

# File path for saving data locally on your laptop
chat_file = f"chat_history_{user_name}.txt"

st.sidebar.markdown("---")
st.sidebar.subheader(f"History for: {user_name.capitalize()}")

# --- Line 23 se start karo aur purana kachra saaf kar do ---
if "history" not in st.session_state:
    st.session_state.history = []

if os.path.exists(chat_file):
    with open(chat_file, "r", encoding="utf-8") as file:
        st.sidebar.text_area("Old Records:", file.read(), height=400)
else:
    st.sidebar.info("No previous history found for this user.")

# --- Iske neeche seedha Line 38 (st.title) shuru honi chahiye ---

# --- 4. CHAT INTERFACE ---
st.title("🤖 Sammad's Universal AI Server")
st.write(f"Active User: **{user_name.capitalize()}**")

# Session state to keep chat visible on screen
if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying the chat on screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. LOGIC & SAVING ---
if prompt := st.chat_input("Type your question..."):
    # Display user input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Permanent Save to Laptop (User's question)
    with open(chat_file, "a", encoding="utf-8") as f:
        f.write(f"USER: {prompt}\n")

    # Generate AI Answer
    with st.chat_message("assistant"):
        # Explicit instruction for long, detailed answers
        context = f"Instruction: Provide a very detailed, long, and expert response. Question: {prompt}"
        response = model.generate_content(context)
        st.markdown(response.text)
    
    # Permanent Save to Laptop (AI's answer)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    with open(chat_file, "a", encoding="utf-8") as f:
        f.write(f"AI: {response.text}\n{'-'*30}\n")
