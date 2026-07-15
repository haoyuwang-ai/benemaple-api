import os
from pathlib import Path

from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.embeddings.openai import OpenAIEmbedding

from pipeline.node_store import load_nodes_jsonl

def get_embedding_model() -> OpenAIEmbedding:
    model_name = os.getenv(
        "OPENAI_EMBED_MODEL",
        "text-embedding-3-small",
    )

    return OpenAIEmbedding(model=model_name, 
                           api_key=os.getenv("OPENAI_API_KEY"),
                           api_base=os.getenv("OPENAI_BASE_URL"))


def build_vector_index(
    nodes_path: Path = Path("data/nodes/nodes.jsonl"),
    persist_dir: Path = Path("data/index"),
) -> VectorStoreIndex:
    nodes = list(load_nodes_jsonl(nodes_path))
    embed_model = get_embedding_model()

    index = VectorStoreIndex(
        nodes,
        embed_model=embed_model,
        show_progress=True,
    )

    index.storage_context.persist(
        persist_dir=str(persist_dir)
    )

    return index


def load_vector_index(
    persist_dir: Path = Path("data/index"),
):
    storage_context = StorageContext.from_defaults(
        persist_dir=str(persist_dir)
    )

    return load_index_from_storage(
        storage_context,
        embed_model=get_embedding_model(),
    )   
