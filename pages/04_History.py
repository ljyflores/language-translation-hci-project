import os
import streamlit as st
from streamlit_float import float_init  # type: ignore
from utils import (
    read_list_of_dicts_from_json,
    get_suggestion_answer_advanced,
    get_feedback_answer_advanced,
)


def main():
    # Read in conversation history if available, otherwise create a new dictionary
    if os.path.exists("assets/history.json"):
        history_list = read_list_of_dicts_from_json("assets/history.json")
    else:
        history_list = list[dict[str, str]]()

    # Name the pages and tab bar
    st.set_page_config(page_title="Hello", page_icon="👋")

    # Initialize floating features for the interface
    float_init()

    st.title("History Mode")
    if history_list:
        print(history_list)
        num_suggestions = 0
        num_feedback = 0

        for item in history_list:
            if item["role"] == "User" or item["role"] == "Partner Speaker":
                st.markdown("---")
                st.markdown(f":green[**{item['role']}**] :  \n {item['content']}")  # type: ignore

            elif item["role"] == "Feedback LLM":
                num_feedback += 1
                st.markdown(f":blue[**{item['role']}**] :  \n {item['content']}")
                if st.button("Advanced Feedback", key=f"feedback{num_feedback}"):
                    message = [{"role": "user", "content": item["content"]}]
                    llm_advanced_feedback = (
                        get_feedback_answer_advanced(message, "gpt-4o-mini")
                        or "No response given!"
                    )
                    st.markdown(
                        f":blue[**{item['role']}**] :  \n {llm_advanced_feedback}"
                    )

            elif item["role"] == "Suggestion LLM":
                num_suggestions += 1
                st.markdown(f":blue[**{item['role']}**] :  \n {item['content']}")
                if st.button("Advanced Suggestion", key=f"suggestion{num_suggestions}"):
                    message = [{"role": "user", "content": item["content"]}]
                    llm_advanced_suggestions = (
                        get_suggestion_answer_advanced(message, "gpt-4o-mini")
                        or "No response given!"
                    )
                    st.markdown(f":blue[**{item['role']}**] :  \n {llm_advanced_suggestions}")  # type: ignore
    else:
        st.write("No conversation history to show!")  # type: ignore


if __name__ == "__main__":
    main()
