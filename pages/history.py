import os
import streamlit as st
from streamlit_float import float_init  # type: ignore
from utils import read_list_of_dicts_from_json


# Read in conversation history if available, otherwise create a new dictionary
if os.path.exists("assets/history.json"):
    history_list = read_list_of_dicts_from_json("assets/history.json")
else:
    history_list = list[dict[str, str]]()

# Name the pages and tab bar
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.sidebar.success("Mode Selection")

# Initialize floating features for the interface
float_init()

st.title("Conversation History 🤖")
if history_list:
    print(history_list)
    for item in history_list:
        st.write(f"{item['role']}: {item['content']}")  # type: ignore
else:
    st.write("No conversation history to show!")  # type: ignore
