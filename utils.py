import json
from typing import Literal, cast
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_KEY"])


def speech_to_text(audio_data: str):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", response_format="text", file=audio_file
        )
    return transcript


def get_suggestion_answer(
    messages: list[dict[str, str]], model: Literal["gpt-3.5-turbo-1106"]
):
    system_message = [
        {
            "role": "system",
            "content": "You are an helpful AI chatbot, that answers questions asked by User.",
        }
    ]
    messages = system_message + messages
    try:
        response = client.chat.completions.create(model=model, messages=messages)  # type: ignore
        return response.choices[0].message.content
    except:
        return "Hello from the other side"


def get_feedback_answer(
    messages: list[dict[str, str]], model: Literal["gpt-3.5-turbo-1106"]
):
    system_message = [
        {
            "role": "system",
            "content": "You are an helpful AI chatbot, that answers questions asked by User.",
        }
    ]
    messages = system_message + messages
    try:
        response = client.chat.completions.create(model=model, messages=messages)  # type: ignore
        return response.choices[0].message.content
    except:
        return "Hello from the other side"


def read_list_of_dicts_from_json(json_path: str):
    with open(json_path, "r") as file:
        result = json.load(file)
        result = [cast(dict[str, str], dictionary) for dictionary in result]
        return result


def save_list_of_dicts_to_json(json_path: str, list_of_dicts: list[dict[str, str]]):
    with open(json_path, "w") as file:
        file.write(json.dumps(list_of_dicts, indent=4))
