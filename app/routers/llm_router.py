import os

from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from app.llm.schema import TaskAnalyzeInput, TaskAnalyzeOutput


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

    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="LLM integration not enabled yet"
    )