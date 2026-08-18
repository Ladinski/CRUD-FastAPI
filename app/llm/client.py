import json
import os
import random
import time
from pathlib import Path

import openai
from openai import OpenAI
from pydantic import ValidationError

from app.llm.schema import TaskAnalyzeOutput


BASE_DIR = Path(__file__).resolve().parents[2]
PROMPT_PATH = BASE_DIR / "prompts" / "task-analyze-v1.md"
QUARANTINE_PATH = BASE_DIR / "logs" / "quarantine.jsonl"

PROMPT_VERSION = "task-analyze-v1"

client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY"),
    timeout=30.0,
    max_retries=0
)


def call_model(messages, repair=False):
    max_attempts = 3

    for attempt in range(max_attempts):
        start_time = time.perf_counter()

        try:
            response = client.chat.completions.create(
                model=os.getenv("LLM_MODEL"),
                temperature=0.2,
                messages=messages
            )

            duration_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2
            )

            usage = response.usage

            log_entry = {
                "prompt_version": PROMPT_VERSION,
                "model": os.getenv("LLM_MODEL"),
                "input_tokens": usage.prompt_tokens if usage else None,
                "output_tokens": usage.completion_tokens if usage else None,
                "duration_ms": duration_ms,
                "repair": repair
            }

            print(json.dumps(log_entry))

            return response.choices[0].message.content

        except openai.APITimeoutError:
            if attempt == max_attempts - 1:
                raise

        except openai.RateLimitError:
            if attempt == max_attempts - 1:
                raise

        except openai.APIStatusError as error:
            if error.status_code < 500:
                raise

            if attempt == max_attempts - 1:
                raise

        wait_time = (2 ** attempt) + random.uniform(0, 0.5)
        time.sleep(wait_time)


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
        "prompt_version": PROMPT_VERSION
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

    raw_output = call_model(
        messages,
        repair=False
    )

    try:
        return validate_output(raw_output)

    except (
        ValueError,
        json.JSONDecodeError,
        ValidationError
    ) as error:

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

        repaired_output = call_model(
            repair_messages,
            repair=True
        )

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