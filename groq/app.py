import streamlit as st
import requests
import streamlit.components.v1 as components

# Groq API config
API_KEY =st.secrets["API_KEY"]
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192" 

# Streamlit config
st.set_page_config(page_title="Groq Chatbot", layout="centered")
st.markdown("<h1 style='text-align: center;'>🤖 Groq LLM Chatbot</h1>", unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", key="input", label_visibility="collapsed", placeholder="Type a message and press Enter")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    st.session_state.chat_history.append(("user", user_input))

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": user_input}]
    }

    try:
        response = requests.post(API_URL, headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }, json=data)
        response.raise_for_status()
        ai_response = response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        ai_response = f"⚠️ Error: {e}"

    st.session_state.chat_history.append(("assistant", ai_response))

# Show chat history
for role, message in st.session_state.chat_history:
    bg_color = "#33a8ff" if role == "user" else "#ff5733"
    role_label = "You" if role == "user" else "AI"
    st.markdown(f"""
        <div style='background-color: {bg_color}; padding: 10px; border-radius: 10px; margin-bottom: 10px'>
            <b>{role_label}:</b><br>{message}
        </div>
    """, unsafe_allow_html=True)

# ✅ Add auto-scroll at the bottom
components.html("""
    <script>
        const chatBox = window.parent.document.querySelector('.main');
        chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
    </script>
""", height=0)
