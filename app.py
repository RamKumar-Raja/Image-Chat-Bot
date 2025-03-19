import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import PIL.Image
import time

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key="AIzaSyArsv1opSupAk53gRzy3cbCCfWKW7yOiBs")

# Configure Streamlit page
st.set_page_config(page_title="Vision Chat Pro", layout="wide")

# Custom CSS for improved UI
st.markdown(
    """
    <style>
        .chat-container { height: 65vh; overflow-y: auto; padding: 10px; }
        .message-box { padding: 12px; border-radius: 10px; margin-bottom: 10px; max-width: 80%; }
        .user-msg { background-color: #2d4059; color: white; align-self: flex-end; }
        .bot-msg { background-color: #222831; color: white; align-self: flex-start; }
        .chat-box { display: flex; flex-direction: column; }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title
st.title("🖼️ Vision Chat Pro")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

# Layout with sidebar for image upload
with st.sidebar:
    st.header("📤 Upload Image")
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        try:
            st.session_state.uploaded_image = PIL.Image.open(uploaded_file)
            st.image(st.session_state.uploaded_image, use_container_width=True, caption="Uploaded Image")
            st.success("✅ Image uploaded successfully!")
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")

# Chat UI
st.subheader("💬 Chat Interface")
chat_container = st.container()

# Display chat messages
with chat_container:
    chat_box = """<div class='chat-box'>"""
    for message in st.session_state.messages:
        role_class = "user-msg" if message["role"] == "user" else "bot-msg"
        chat_box += f"<div class='message-box {role_class}'><b>{message['role'].title()}:</b> {message['content']}</div>"
    chat_box += "</div>"
    st.markdown(chat_box, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask about the image..."):
    if not st.session_state.uploaded_image:
        st.warning("Please upload an image first!")
        st.stop()
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Processing animation
    with st.spinner("🔍 Analyzing image..."):
        time.sleep(0.5)
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=[prompt, st.session_state.uploaded_image]
                
            )
            time.sleep(0.5)
            
            if response.text:
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("No response generated")
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")
    
    st.rerun()