from typing import Any

from pydantic import BaseModel, Field


# 问题格式
class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    profile: dict[str, Any] = Field(default_factory=dict)

# 引用格式
class SourceResponse(BaseModel):
    score: float | None = None
    title: str
    section: str
    url: str

# 回答格式
class QuestionResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]