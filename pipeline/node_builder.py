from pathlib import Path

from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.schema import BaseNode

from pipeline.catalog_loader import iter_catalog_entries
from pipeline.document_builder import catalog_entry_to_document


def build_nodes(
    catalog_path: Path = Path("data/catalog/documents.jsonl"),
) -> list[BaseNode]:
    documents = [
        catalog_entry_to_document(entry)
        for entry in iter_catalog_entries(catalog_path)
    ]

    pipeline = IngestionPipeline(
        transformations=[
            MarkdownNodeParser.from_defaults(
                include_metadata=True,
                include_prev_next_rel=True,
            )
        ]
    )

    return list(pipeline.run(documents=documents))
