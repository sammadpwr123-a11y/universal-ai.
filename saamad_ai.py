import streamlit as st
import google.generativeai as genai
import os

# API Key setup from Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Setup Error: {e}")

st.title("🚀 Sammad's Universal AI Server bestfreind hasnain aak lora bhan ka ")

if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar history
st.sidebar.title("Chat History")
for chat in st.session_state.history:
    st.sidebar.write(f"**You:** {chat['user']}")
    st.sidebar.write(f"**AI:** {chat['ai']}")
    st.sidebar.markdown("---")

# Main chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    try:
        response = model.generate_content(user_input)
        ai_response = response.text
        
        # Save to history
        st.session_state.history.append({"user": user_input, "ai": ai_response})
        
        # Display current chat
        st.write(f"**You:** {user_input}")
        st.write(f"**AI:** {ai_response}")
    except Exception as e:
        st.error(f"AI Error: {e}")
