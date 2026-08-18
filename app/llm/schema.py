from enum import Enum

from pydantic import BaseModel, Field


class TaskCategory(str, Enum):
    work = "work"
    study = "study"
    personal = "personal"
    other = "other"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskAnalyzeInput(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class TaskAnalyzeOutput(BaseModel):
    category: TaskCategory
    priority: TaskPriority
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str