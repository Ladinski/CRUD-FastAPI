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

    try:
        return analyze_task_with_llm(data.text)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Model could not produce a valid response"
        )