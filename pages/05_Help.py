import streamlit as st

from streamlit_float import float_init  # type: ignore

# Name the pages and tab bar
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

# Initialize floating features for the interface
float_init()


st.title("Help Guide")

st.subheader("Suggest and Feedback Mode")
st.write(
    "Suggest Mode is used to receive suggestions for how to respond to what the other person is saying"
)
st.write(
    "Feedback Mode is used to get feedback on how to improve the grammar and correctness of what you said"
)

st.subheader("Usage")
st.write(
    "**Suggest Mode**: Press the microphone when the partner speaker is talking, to get a response"
)
st.write(
    "**Feedback Mode**: Press the microphone when you are talking, to get feedback"
)

st.subheader("Surroundings Translation")

st.write(
    "Surroundings translation is used to read and translate signs and name objects in a foreign language. Click the capture button to capture what you see and get the model's translations!"
)
