import streamlit as st
import google.generativeai as genai
import os

# --- 1. API Setup with Multi-Model Power ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Hum ne yahan sabse stable model rakha hai jo 3.1 jaisa fast hai
    # Agar ye fail hua toh 'gemini-pro' chal jayega
    model_name = 'gemini-1.5-flash-latest' 
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 2. Permanent Storage (Server File) ---
chat_file = "permanent_storage.txt"

def save_to_server(u, a):
    with open(chat_file, "a", encoding="utf-8") as f:
        f.write(f"USER: {u}\nAI: {a}\n" + "-"*30 + "\n")

def read_from_server():
    if os.path.exists(chat_file):
        with open(chat_file, "r", encoding="utf-8") as f:
            return f.read()
    return "Abhi tak koi data save nahi hua."

# --- 3. Professional UI ---
st.set_page_config(page_title="Sammad AI Pro", page_icon="🚀")
st.title("🚀 Sammad's High-Power AI Server")
st.info("System Status: Permanent Record & High-Speed Models Active")

# --- 4. Sidebar (Memory Management) ---
with st.sidebar:
    st.title("📜 Permanent Logs")
    if st.button("Format Server (Delete All)"):
        if os.path.exists(chat_file):
            os.remove(chat_file)
            st.rerun()
    st.text_area("Full Chat Memory:", read_from_server(), height=500)

# --- 5. High-Speed Chat Interface ---
user_input = st.chat_input("Ask me anything (I will remember this forever)...")

if user_input:
    try:
        # Generating response
        response = model.generate_content(user_input)
        final_text = response.text
        
        # Saving permanently
        save_to_server(user_input, final_text)
        
        # Displaying results
        st.write(f"**You:** {user_input}")
        st.write(f"**AI:** {final_text}")
        
        # Update sidebar
        st.rerun()
    except Exception as e:
        # Agar latest model na chale, toh purane stable par switch karo
        st.warning("Switching to Stable Core... Please try again.")
        model = genai.GenerativeModel('gemini-pro')
        st.error(f"Error Details: {e}")
