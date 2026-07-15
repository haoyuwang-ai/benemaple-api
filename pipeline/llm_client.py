import os

from llama_index.llms.openai import OpenAI


def get_llm() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing")

    model_name = os.getenv(
        "OPENAI_MODEL",
        "gpt-5.4-nano",
    )

    return OpenAI(
        model=model_name,
        api_key=api_key,
        api_base=os.getenv("OPENAI_BASE_URL"),
    )