import os
import streamlit as st

from audio_recorder_streamlit import audio_recorder  # type: ignore
from streamlit_float import float_init  # type: ignore
from streamlit_js_eval import streamlit_js_eval
from utils import (
    get_suggestion_answer,
    get_translation,
    speech_to_text,
    read_list_of_dicts_from_json,
    save_list_of_dicts_to_json,
)

# Read in conversation history if available, otherwise create a new dictionary
if os.path.exists("assets/history.json"):
    history_list = read_list_of_dicts_from_json("assets/history.json")
else:
    history_list = list[dict[str, str]]()
    save_list_of_dicts_to_json("assets/history.json", history_list)

# Name the pages and tab bar
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

# Initialize floating features for the interface
float_init()


# Initialize session state for managing chat messages
if "messages" not in st.session_state:
    st.session_state.messages = list[dict[str, str]]()


st.title("Suggestion Mode")

# Create a container for the microphone and audio recording
footer_container = st.container()
with footer_container:
    st.write("Press when the partner speaker is talking!")
    audio_bytes = audio_recorder()

if audio_bytes:
    # Speech to text
    with st.spinner("Transcribing..."):
        # Write the audio bytes to a temporary file
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        # Convert the audio to text using the speech_to_text function
        try:
            transcript = speech_to_text(webm_file_path)
        except:
            transcript = "Audio could not be transcribed!"

    # Save text
    if transcript:
        # Output message on screen
        st.session_state.messages.append({"role": "user", "content": transcript})
        st.chat_message("user").markdown(transcript)
        os.remove(webm_file_path)
        # Save partner speaker message to history
        history_list.append({"role": "Partner Speaker", "content": transcript})
        save_list_of_dicts_to_json("assets/history.json", history_list)

    # Get LLM response
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):
            llm_str_translation = (
                get_translation(st.session_state.messages, "gpt-4o-mini")
                or "No response given!"
            )

            llm_str_suggestion = (
                get_suggestion_answer(st.session_state.messages, "gpt-4o-mini")
                or "No response given!"
            )

        # Output message on screen
        st.write("#### :blue[**Translation:**] " + llm_str_translation)  # type: ignore
        st.write("#### :green[**Suggested Response:**] " + llm_str_suggestion)
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": llm_str_translation + "\n" + llm_str_suggestion,
            }
        )
        # Save LLM response to history
        history_list.append(
            {
                "role": "Suggestion LLM",
                "content": "Translation: "
                + llm_str_translation
                + "  \n"
                + "Suggested Response: "
                + llm_str_suggestion,
            }
        )
        save_list_of_dicts_to_json("assets/history.json", history_list)

if st.button("Clear Page"):
    streamlit_js_eval(js_expressions="parent.window.location.reload()")
