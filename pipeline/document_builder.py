from pathlib import Path
from typing import Any

from llama_index.core import Document


def catalog_entry_to_document(entry: dict[str, Any]) -> Document:
    """根据 catalog 记录和本地 Markdown 构建 LlamaIndex Document。"""

    markdown_path = Path(entry["local_markdown_path"])
    markdown = markdown_path.read_text(encoding="utf-8")

    parser_info = entry.get("parser", {})
    metadata = {
        "document_id": entry["document_id"],
        "title": entry["title"],
        "source_url": entry["source_url"],
        "source_type": entry["source_type"],
        "jurisdiction": entry["jurisdiction"],
        "language": entry["language"],
        "retrieved_at": entry.get("retrieved_at"),
        "parser_provider": parser_info.get("provider"),
        "parser_tier": parser_info.get("tier"),
        "parser_version": parser_info.get("version"),
    }
    metadata = {
        key: value
        for key, value in metadata.items()
        if value is not None
    }

    return Document(
        text=markdown,
        doc_id=entry["document_id"],
        metadata=metadata,
        # 这些字段仍保留在 node.metadata 中，
        # 但不参与 embedding，避免污染语义向量。
        excluded_embed_metadata_keys=[
            "document_id",
            "source_url",
            "source_type",
            "language",
            "retrieved_at",
            "parser_provider",
            "parser_tier",
            "parser_version",
        ],
    )
