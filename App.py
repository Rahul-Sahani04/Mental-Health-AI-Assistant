import streamlit as st
import os
from dotenv import load_dotenv
import json
import google.generativeai as genai

import base64
from PIL import Image
from io import BytesIO

load_dotenv()

api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    api_key = st.secrets["GENAI_API_KEY"]
    if not api_key:
        st.error("Please set the GENAI_API_KEY environment variable.")
        st.stop()

genai.configure(api_key=api_key)

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 8192,
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

img_file_buffer = None
CameraButton = True

# Button to open the camera
if st.button("Open Camera", key="Camera"):
    CameraButton = not CameraButton
    # Take a picture using the camera input

img_file_buffer = st.camera_input(
    "Take a picture",
    disabled=CameraButton,
    help="Let the AI take a photo and analyse your Mood & Facial Expression. Refresh the page and allow camera access if this doesn't works.",
)

# Check if an image has been taken
if img_file_buffer is not None:
    vision_model = genai.GenerativeModel(
        model_name="gemini-pro-vision",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    vision_model.start_chat(history=conversation_history)

    # Display the taken image
    # st.image(img_file_buffer, caption="Taken Image", use_column_width=True)

    # Convert the image to bytes
    img_pil = Image.open(img_file_buffer)
    img_io = BytesIO()
    img_pil.save(img_io, format="JPEG")
    img_bytes = img_io.getvalue()

    # Encode image bytes to base64
    encoded_img = base64.b64encode(img_bytes).decode("utf-8")

    # Set up image parts for the model
    image_parts = [
        {"mime_type": "image/jpeg", "data": encoded_img},
    ]

    # Prompt for the model
    prompt_parts = [
        """Examine the facial expression, mood, and mental well-being conveyed in the given image. Present the outcomes in markdown format as follows:
            **Facial Expression:** {Predicted facial expression by the model}.  \n
            **Mood:** {Predicted mood by the model}.  \n
            **Mental Health:** {Model-generated assessment of mental health}.
        """,
        image_parts[0],
    ]

    # Generate content using the model
    response = vision_model.generate_content(prompt_parts)

    # Display the model's response
    st.write(response.text)
    img_file_buffer.close()
