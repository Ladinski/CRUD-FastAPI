import json
import os
from pathlib import Path

from openai import OpenAI
from pydantic import ValidationError

from app.llm.schema import TaskAnalyzeOutput


BASE_DIR = Path(__file__).resolve().parents[2]
PROMPT_PATH = BASE_DIR / "prompts" / "task-analyze-v1.md"
QUARANTINE_PATH = BASE_DIR / "logs" / "quarantine.jsonl"

client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY")
)


def call_model(messages):
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        temperature=0.2,
        messages=messages
    )

    return response.choices[0].message.content


def extract_json(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found")

    return text[start:end + 1]


def validate_output(raw_output: str) -> TaskAnalyzeOutput:
    json_text = extract_json(raw_output)

    data = json.loads(json_text)

    return TaskAnalyzeOutput.model_validate(data)


def quarantine(
    input_text: str,
    raw_output: str,
    error: str
):
    QUARANTINE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    entry = {
        "input": input_text,
        "raw_output": raw_output,
        "error": error,
        "prompt_version": "task-analyze-v1"
    }

    with QUARANTINE_PATH.open(
        "a",
        encoding="utf-8"
    ) as file:
        file.write(json.dumps(entry) + "\n")


def analyze_task_with_llm(text: str) -> TaskAnalyzeOutput:
    system_prompt = PROMPT_PATH.read_text(
        encoding="utf-8"
    )

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": text
        }
    ]

    raw_output = call_model(messages)

    try:
        return validate_output(raw_output)

    except (ValueError, json.JSONDecodeError, ValidationError) as error:
        repair_messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": text
            },
            {
                "role": "assistant",
                "content": raw_output
            },
            {
                "role": "user",
                "content": (
                    "Your previous answer was rejected for this reason:\n"
                    f"{error}\n\n"
                    "Return only corrected JSON matching the required schema."
                )
            }
        ]

        repaired_output = call_model(repair_messages)

        try:
            return validate_output(repaired_output)

        except (
            ValueError,
            json.JSONDecodeError,
            ValidationError
        ) as second_error:

            quarantine(
                input_text=text,
                raw_output=repaired_output,
                error=str(second_error)
            )

            raise ValueError(
                "Model could not produce a valid response"
            )