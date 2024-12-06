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
    "Suggest Mode": "pages/01_Suggest_Mode.py",
    "Feedback Mode": "pages/02_Feedback_Mode.py",
    "Surrounding Mode": "pages/03_Surrounding_Mode.py",
    "History": "pages/04_History.py",
    "Help": "pages/05_Help.py",
}

# Get root path from session state
root_path = os.path.dirname(os.path.abspath(__file__)).strip("/pages")

# Show available modes
mode_list = ["Suggest Mode", "Feedback Mode", "Surrounding Mode", "History", "Help"]

caption_list = [
    "Get model suggestions to continue the conversation",
    "Get feedback on how you can improve your conversation",
    "Real-time translation of your surroundings",
    "View conversation history",
    "Get help on how to use the tool",
]

selected_mode = st.radio(
    "Select a Mode", mode_list, captions=caption_list, key="task_select_button"
)

# Go to task
if st.button("Go to Mode!", key="task_begin_button"):
    st.switch_page(option_to_page_mapping[selected_mode])
