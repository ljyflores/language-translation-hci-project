import json
from typing import Literal, cast
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_KEY"])


def speech_to_text(audio_data: str):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", response_format="text", file=audio_file
        )
    return transcript


def get_translation(
    messages: list[dict[str, str]], model: Literal["gpt-3.5-turbo-1106"]
):
    system_message = [
        {
            "role": "system",
            "content": "Translate the following text from Chinese to English. Ensure the translation is clear, natural, and accurate, maintaining the original tone and intent. Avoid adding extra explanations or modifying the meaning.",
        }
    ]

    try:
        response = client.chat.completions.create(model=model, messages=system_message + [messages[-1]])  # type: ignore
        return response.choices[0].message.content
    except:
        return "API Error: Error retrieving translation!"


def get_suggestion_answer(
    messages: list[dict[str, str]], model: Literal["gpt-3.5-turbo-1106"]
):
    system_message = [
        {
            "role": "system",
            "content": "Provide in Chinese a response format or template for answering the given question, using blanks (e.g., ____) to indicate where detailed content should be filled in. In the second line, give the pinyin of the Chinese template. In the third line, directly give the English translation of the Chinese template.",
        }
    ]

    try:
        response = client.chat.completions.create(model=model, messages=system_message + [messages[-1]])  # type: ignore
        return response.choices[0].message.content
    except:
        return "API Error: Error retrieving suggestion!"


def get_feedback_answer(
    messages: list[dict[str, str]], model: Literal["gpt-3.5-turbo-1106"]
):
    system_message = [
        {
            "role": "system",
            "content": "Analyze the following input text for errors in grammar or word usage. For each error found: firstly highlight the error using a specific marker (e.g., enclose it in ** for emphasis). Secondly, in the next line, provide a brief explanation of the error. Thirdly, in the next line, offer the corrected version."
            + "\n"
            + "List each error on a new line, with its corresponding explanation and correction. Give your analysis mostly in English",
        }
    ]

    try:
        response = client.chat.completions.create(model=model, messages=system_message + [messages[-1]])  # type: ignore
        return response.choices[0].message.content
    except:
        return "API Error: Error retrieving feedback!"


def get_suggestion_answer_advanced(
    messages: list[dict[str, str]], model: Literal["gpt-3.5-turbo-1106"]
):
    system_message = [
        {
            "role": "system",
            "content": "Provide in Chinese several different response formats or templates for answering the given question, using blanks (e.g., ____) to indicate where detailed content should be filled in. For each template, in the next line, give the pinyin of the Chinese template, and in another line, directly give the English translation of the Chinese template. Make sure each template is significantly different from each other.",
        }
    ]

    try:
        response = client.chat.completions.create(model=model, messages=system_message + [messages[-1]])  # type: ignore
        return response.choices[0].message.content
    except:
        return "API Error: Error retrieving suggested answer!"


def get_feedback_answer_advanced(
    messages: list[dict[str, str]], model: Literal["gpt-3.5-turbo-1106"]
):
    system_message = [
        {
            "role": "system",
            "content": "Analyze the following input text for errors in grammar or word usage. Give a very detailed analysis including explanation, multiple possible corrections and examples of similar errors."
            + "\n"
            + "List each error on a new line, with its corresponding explanation, corrections and similar error examples. Give your analysis mostly in English",
        }
    ]

    try:
        response = client.chat.completions.create(model=model, messages=system_message + [messages[-1]])  # type: ignore
        return response.choices[0].message.content
    except:
        return "API Error: Error retrieving feedback!"


def encode_image(image_path: str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_surrounding_objects(
    image_path: str, model: Literal["gpt-3.5-turbo-1106", "gpt-4o"]
):
    base64_image = encode_image(image_path)

    system_message = [
        {
            "role": "system",
            "content": "You are an helpful AI chatbot, that answers questions asked by User.",
        }
    ]

    image_message = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Detect and list the name of all the objects in the image in English. Put the Chinese translation along each English name. Do not add any other text.",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ]

    try:
        response = client.chat.completions.create(model=model, messages=system_message + image_message)  # type: ignore
        return response.choices[0].message.content
    except:
        return None


def read_list_of_dicts_from_json(json_path: str):
    with open(json_path, "r") as file:
        result = json.load(file)
        result = [cast(dict[str, str], dictionary) for dictionary in result]
        return result


def save_list_of_dicts_to_json(json_path: str, list_of_dicts: list[dict[str, str]]):
    with open(json_path, "w") as file:
        file.write(json.dumps(list_of_dicts, indent=4))
