from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Any

app = FastAPI()

# 问题格式
class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    profile: dict[str, Any] = Field(default_factory=dict)

# 回答格式
class QuestionResponse(BaseModel):
    answer: str


@app.get("/")
def read_root():
    return {"message": "BeneMaple API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/questions", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    return QuestionResponse(
        answer=f"暂时的模拟回答：你问的是「{request.question}」"
    )