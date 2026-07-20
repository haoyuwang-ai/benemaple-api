from llama_index.core import PromptTemplate
from llama_index.core.base.base_query_engine import BaseQueryEngine

from pipeline.llm_client import get_llm
from pipeline.vector_index import load_vector_index


QA_PROMPT = PromptTemplate(
    """
You are a Canadian benefits assistant.

Use only the context below to answer the question.
Do not use outside knowledge.
If the context does not contain enough information,
say that the available documents do not provide the answer.
Answer in the same language as the question.

Context:
---------------------
{context_str}
---------------------

Question: {query_str}

Answer:
""".strip()
)


def create_query_engine(
    *,
    streaming: bool = False,
) -> BaseQueryEngine:
    index = load_vector_index()
    llm = get_llm()

    return index.as_query_engine(
        llm=llm,
        similarity_top_k=3,
        response_mode="simple_summarize",
        text_qa_template=QA_PROMPT,
        streaming=streaming,
    )