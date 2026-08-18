import os

from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from app.llm.schema import TaskAnalyzeInput, TaskAnalyzeOutput

from app.llm.client import analyze_task_with_llm

router = APIRouter(
    prefix="/tasks",
    tags=["AI"]
)


@router.post(
    "/analyze",
    response_model=TaskAnalyzeOutput,
    summary="Analyze a task",
    description="Classifies a task into a category and priority."
)
async def analyze_task(data: TaskAnalyzeInput):
    if os.getenv("LLM_STUB") == "1":
        return TaskAnalyzeOutput(
            category="study",
            priority="medium",
            confidence=0.95,
            reason="Stub response for development."
        )

    result = analyze_task_with_llm(data.text)

    return {
        "category": "other",
        "priority": "low",
        "confidence": 0.0,
        "reason": result
    }