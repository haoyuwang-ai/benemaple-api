from fastapi import FastAPI
from app.schemas import QuestionRequest, QuestionResponse
from app.source_builder import build_sources

from dotenv import load_dotenv

from pipeline.rag_query import create_query_engine

load_dotenv()

app = FastAPI()

query_engine = create_query_engine()

@app.get("/")
def read_root():
    return {"message": "BeneMaple API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/questions", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    response = query_engine.query(request.question)

    sources = build_sources(response.source_nodes)

    return QuestionResponse(
        answer=str(response),
        sources=sources,
    )