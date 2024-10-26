import os
import streamlit as st

from utils import get_answer, speech_to_text
from audio_recorder_streamlit import audio_recorder  # type: ignore
from streamlit_float import float_init  # type: ignore

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.sidebar.success("Mode Selection")

# Initialize floating features for the interface
float_init()


# Initialize session state for managing chat messages
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = list[dict[str, str]]()


# Create a container for the microphone and audio recording
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()
initialize_session_state()

st.title("OpenAI Conversational Chatbot 🤖")

if audio_bytes:
    with st.spinner("Transcribing..."):
        # Write the audio bytes to a temporary file
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        # Convert the audio to text using the speech_to_text function
        transcript = speech_to_text(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)  # type: ignore
            os.remove(webm_file_path)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):
            final_response = get_answer(st.session_state.messages, "gpt-3.5-turbo-1106")
        st.write(final_response or "No response given!")  # type: ignore
        st.session_state.messages.append(
            {"role": "assistant", "content": final_response}
        )
