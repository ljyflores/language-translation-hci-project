import os
import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

option_to_page_mapping = {
    "Suggest Mode": "pages/chat_suggest.py",
    "Feedback Mode": "pages/chat_feedback.py",
    "Voice Commands Mode": "pages/voice.py",
}

# Get root path from session state
root_path = os.path.dirname(os.path.abspath(__file__)).strip("/pages")

# Show available modes
mode_list = ["Suggest Mode", "Feedback Mode", "Voice Commands Mode"]

caption_list = [
    "Get model suggestions to continue the conversation",
    "Get feedback on how you can improve your conversation",
    "Use voice commands to read and translate your surroundings",
]

selected_mode = st.radio(
    "Select a Mode", mode_list, captions=caption_list, key="task_select_button"
)

# Go to task
if st.button("Begin Task", key="task_begin_button"):
    st.switch_page(option_to_page_mapping[selected_mode])
