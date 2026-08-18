import os
import openai

from fastapi import APIRouter, HTTPException, status

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

    if os.getenv("LLM_ENABLED", "true").lower() == "false":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM feature is currently disabled"
        )

    try:
        return analyze_task_with_llm(data.text)

    except openai.APITimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="LLM provider timed out"
        )

    except openai.RateLimitError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM provider rate limit reached"
        )

    except openai.APIStatusError as error:
        if error.status_code in (400, 401, 403):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="LLM provider request failed"
            )

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM provider unavailable"
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Model could not produce a valid response"
        )