import os
import streamlit as st
from utils import get_surrounding_objects

# Name the pages and tab bar
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("Surroundings Translation Mode")

picture = st.camera_input("", label_visibility="collapsed")

if picture:
    with open("assets/image.jpg", "wb") as file:
        file.write(picture.getbuffer())
    with st.spinner("Thinking🤔..."):
        llm_str_response = get_surrounding_objects(
            image_path="assets/image.jpg", model="gpt-4o"
        )
    if llm_str_response:
        st.write(f"#### {llm_str_response}")
    else:
        st.write(f"#### API Error!")
