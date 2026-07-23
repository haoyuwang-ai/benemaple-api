import os
import secrets

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas import QuestionRequest, QuestionResponse
from app.source_builder import build_sources

from dotenv import load_dotenv

from pipeline.rag_query import create_query_engine

from app.sse import sse_event

load_dotenv()

# Internal token authentication dependency
def require_internal_token(
    x_internal_api_key: str | None = Header(default=None),
) -> None:
    expected_token = os.getenv("API_INTERNAL_TOKEN")

    if not expected_token:
        raise RuntimeError("API_INTERNAL_TOKEN is missing")

    if not secrets.compare_digest(
        x_internal_api_key or "",
        expected_token,
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )
    
app = FastAPI()

query_engine = create_query_engine()

streaming_query_engine = create_query_engine(streaming=True)

@app.get("/")
def read_root():
    return {"message": "BeneMaple API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/questions", 
          response_model=QuestionResponse,
          dependencies=[Depends(require_internal_token)],)
def ask_question(request: QuestionRequest):
    response = query_engine.query(request.question)

    sources = build_sources(response.source_nodes)

    return QuestionResponse(
        answer=str(response),
        sources=sources,
    )

@app.post("/questions/stream",
          dependencies=[Depends(require_internal_token)],)
def stream_question(request: QuestionRequest) -> StreamingResponse:
    response = streaming_query_engine.query(request.question)

    sources = build_sources(response.source_nodes)

    def generate_events():
        for token in response.response_gen:
            if token:
                yield sse_event("token", {"text": token})

        yield sse_event(
            "sources",
            {
                "sources": [
                    source.model_dump()
                    for source in sources
                ]
            },
        )

        yield sse_event("done", {})

    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
        },
    )