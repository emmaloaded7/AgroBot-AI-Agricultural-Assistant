import streamlit as st
from google import genai
from dotenv import load_dotenv
import os


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AgroBot",
    page_icon="🌱"
)


# -----------------------------
# Load API Key
# -----------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    st.error("❌ Gemini API key not found. Check your .env file.")
    st.stop()


# -----------------------------
# Create Gemini Client Once
# -----------------------------
if "client" not in st.session_state:

    st.session_state.client = genai.Client(
        api_key=api_key
    )


# -----------------------------
# Create Chat Session Once
# -----------------------------
if "chat" not in st.session_state:

    st.session_state.chat = (
        st.session_state.client.chats.create(
            model="gemini-flash-latest",

            config={
                "system_instruction": """
You are AgroBot.

You are an AI Agricultural Assistant.

Your expertise includes:

🌱 Crop production
🌿 Plant diseases
🐄 Livestock production
🐓 Animal diseases
🧪 Fertilizer recommendations
🌍 Soil management
💧 Irrigation
🐛 Pest control
🤖 Precision agriculture
♻️ Sustainable agriculture
🧬 Agricultural biotechnology

Always provide professional, practical,
and scientifically based agricultural advice.

If a question is outside agriculture,
politely answer but remind the user that
your main specialization is agriculture.
"""
            }
        )
    )


# -----------------------------
# Initialize Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# App Interface
# -----------------------------
st.title("🌱 AgroBot")

st.write(
    "Your AI Agricultural Assistant powered by Gemini"
)


# Display old messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# User input
prompt = st.chat_input(
    "Ask an agriculture question..."
)


if prompt:

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)


    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # Gemini response
    try:

        response = (
            st.session_state.chat
            .send_message(prompt)
        )

        reply = response.text


    except Exception as e:

        reply = f"""
⚠️ Error communicating with AgroBot:

{e}
"""


    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(reply)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )