# %%
import datetime
import json

from openai import OpenAI

from app.helpers.env_vars import OPENAI_API_KEY
from app.helpers.paths import MESSAGES_DIR
from app.helpers.prompts import SYSTEM_PROMPT
from app.helpers.config import config

from app.tools.load import use_tool

openai_client = OpenAI(api_key=OPENAI_API_KEY)


def save_message(text, role, tool_name=None, tool_args=None):
    dt_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = MESSAGES_DIR / f"{dt_str}.json"
    message = {"role": role, "content": text}

    if tool_name is not None:
        message["tool_name"] = tool_name
    if tool_args is not None:
        message["tool_args"] = tool_args

    with open(path, "w") as f:
        json.dump(message, f, indent=4, ensure_ascii=False)


def load_messages():
    """Loading the last CONVERSATION_LIMIT messages, sorted by filename"""

    messages = []

    for path in sorted(MESSAGES_DIR.glob("*.json"), key=lambda x: x.name)[
        -config.MESSAGE_HISTORY_LENGTH :
    ]:
        with open(path, "r") as f:
            message = json.load(f)

            # Cleaning message to adhere to the format expected by OpenAI's API
            cleaned = {
                "role": message["role"],
                "content": message.get("content", ""),
            }
            if cleaned["content"] is None:
                cleaned["content"] = ""

            # If content is an integer or float, convert it to a string
            if isinstance(cleaned["content"], (int, float)):
                cleaned["content"] = str(cleaned["content"])

            if isinstance(cleaned["content"], (list, dict)):
                cleaned["content"] = json.dumps(cleaned["content"])

            if "tool_name" in message:
                cleaned["name"] = message["tool_name"]

            messages.append(cleaned)

    print(f"Loaded {len(cleaned)} messages with {len(str(cleaned))} characters")
    return messages


def transcribe(path):
    audio_file = open(path, "rb")
    transcription = openai_client.audio.transcriptions.create(
        model="whisper-1", file=audio_file, language="en"
    )

    save_message(transcription.text, "user")

    return transcription.text


from json import JSONDecodeError


def parse_ai_response(raw_ai_response):
    print(f"Parsing AI response: {raw_ai_response}")
    raw_ai_response = raw_ai_response.strip()
    if raw_ai_response.startswith("```json"):
        raw_ai_response = raw_ai_response[7:]
    if raw_ai_response.startswith("```"):
        raw_ai_response = raw_ai_response[3:]
    if raw_ai_response.endswith("```"):
        raw_ai_response = raw_ai_response[:-3]
    raw_ai_response = raw_ai_response.strip()

    # Add functionality to send back errors to AI (while notifying the user of this)
    try:
        json_response = json.loads(raw_ai_response)
    except JSONDecodeError:
        print("JSONDecodeError. Most likely, the AI response is not in JSON format.")
        print(f"AI response: {raw_ai_response}")

        json_response = raw_ai_response

        save_message(raw_ai_response, "assistant", False, None)

        yield raw_ai_response, False, None

    save_message(
        json_response,
        "assistant",
    )

    text = json_response.get("response", "")
    tool = json_response.get("tool_name", None)
    args = json_response.get("tool_args", None)

    yield text, tool, args


# %%


def invoke_ai():
    response = openai_client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
        ]
        + load_messages(),
        temperature=1,
        max_tokens=1024,
        top_p=1,
    )
    for text, tool_name, tool_args in parse_ai_response(
        response.choices[0].message.content
    ):

        if text:
            yield text

        if tool_name:
            tool_response = use_tool(tool_name, tool_args)
            save_message(
                tool_response, "function", tool_name=tool_name, tool_args=tool_args
            )
            yield from invoke_ai()
            return


def generate_audio(text, path):
    with openai_client.audio.speech.with_streaming_response.create(
        model="tts-1", voice="onyx", input=text
    ) as response:
        response.stream_to_file(path)
