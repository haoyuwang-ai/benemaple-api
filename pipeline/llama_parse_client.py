import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from llama_cloud import AsyncLlamaCloud

load_dotenv()


@dataclass
class ParsedDocument:
    source_filename: str
    markdown: str


async def parse_document(file_path: Path) -> ParsedDocument:
    """使用 LlamaParse 将一个本地文件解析为 Markdown。"""

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    api_key = os.getenv("LLAMA_CLOUD_API_KEY")
    if not api_key:
        raise RuntimeError("LLAMA_CLOUD_API_KEY is missing from .env")

    client = AsyncLlamaCloud(api_key=api_key)

    file_obj = await client.files.create(
        file=file_path,
        purpose="parse",
    )

    result = await client.parsing.parse(
        file_id=file_obj.id,
        tier="agentic",
        version="latest",
        expand=["markdown_full"],
    )

    if not result.markdown_full:
        raise RuntimeError("LlamaParse returned no Markdown content")

    # print(result.markdown_full)

    return ParsedDocument(
        source_filename=file_path.name,
        markdown=result.markdown_full,
    )