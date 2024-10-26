from typing import Literal
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


def get_answer(messages: list[dict[str, str]], model: Literal["gpt-3.5-turbo-1106"]):
    system_message = [
        {
            "role": "system",
            "content": "You are an helpful AI chatbot, that answers questions asked by User.",
        }
    ]
    messages = system_message + messages
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content
