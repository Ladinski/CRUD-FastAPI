import os
from pathlib import Path

from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[2]
PROMPT_PATH = BASE_DIR / "prompts" / "task-analyze-v1.md"


client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL"),
    api_key=os.getenv("LLM_API_KEY")
)


def analyze_task_with_llm(text: str) -> str:
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return response.choices[0].message.content