import streamlit as st
import os
from dotenv import load_dotenv
import json
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    st.error("Please set the GENAI_API_KEY environment variable.")
    st.stop()


genai.configure(api_key=st.secrets["GENAI_API_KEY"])

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Load conversation history from file
with open("conversation_history.json", "r") as file:
    conversation_history = json.load(file)

# Start a chat with a greeting and initial information
convo = model.start_chat(history=conversation_history)


welcome_text = "Hello! 😊"
# Display the model's response using Streamlit
st.title("Mental Support Chatbot")
user_input = st.text_input("You:", value=welcome_text)

if st.button("Send", key="SendButton"):
    with st.spinner("Thinking..."):
        convo.send_message(user_input)
        st.caption("Bot's Response:")
        st.write(convo.last.text)
