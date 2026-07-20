from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.schemas import QuestionRequest, QuestionResponse
from app.source_builder import build_sources

from dotenv import load_dotenv

from pipeline.rag_query import create_query_engine

from app.sse import sse_event

load_dotenv()

app = FastAPI()

query_engine = create_query_engine()

streaming_query_engine = create_query_engine(streaming=True)

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

@app.post("/questions/stream")
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