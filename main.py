import os
import streamlit as st

from utils import save_list_of_dicts_to_json

# For each new session, create a new conversation history file
history_list = list[dict[str, str]]()
save_list_of_dicts_to_json("assets/history.json", history_list)


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

option_to_page_mapping = {
    "Suggest Mode": "pages/chat_suggest.py",
    "Feedback Mode": "pages/chat_feedback.py",
    "Voice Commands Mode": "pages/voice.py",
    "History": "pages/history.py",
}

# Get root path from session state
root_path = os.path.dirname(os.path.abspath(__file__)).strip("/pages")

# Show available modes
mode_list = ["Suggest Mode", "Feedback Mode", "Voice Commands Mode", "History"]

caption_list = [
    "Get model suggestions to continue the conversation",
    "Get feedback on how you can improve your conversation",
    "Use voice commands to read and translate your surroundings",
    "View conversation history",
]

selected_mode = st.radio(
    "Select a Mode", mode_list, captions=caption_list, key="task_select_button"
)

# Go to task
if st.button("Begin Task", key="task_begin_button"):
    st.switch_page(option_to_page_mapping[selected_mode])
